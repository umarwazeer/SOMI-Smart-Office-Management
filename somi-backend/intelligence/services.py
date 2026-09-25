from datetime import timedelta

from django.db.models import Avg, Count, Sum
from django.utils import timezone

from attendance.models import Attendance
from employees.models import Employee
from leave.models import LeaveRequest
from payroll.models import Payroll
from performance.models import PerformanceReview
from tasks.models import Task


class IntelligenceEngine:
    """
    Core SOMI intelligence engine.

    This layer uses deterministic application-level analysis
    over existing SOMI operational data.

    It does not access the database through raw SQL and it
    does not depend on an external LLM.
    """

    def __init__(self, user=None):
        self.user = user

    # ---------------------------------------------------------
    # COMMON HELPERS
    # ---------------------------------------------------------

    @staticmethod
    def _decimal_to_float(value):
        if value is None:
            return 0.0

        return float(value)

    @staticmethod
    def _percentage(part, total):
        if not total:
            return 0.0

        return round((part / total) * 100, 2)

    @staticmethod
    def _date_range(days=30):
        today = timezone.localdate()
        start_date = today - timedelta(days=days - 1)

        return start_date, today

    def _can_view_payroll(self):
        if not self.user:
            return False

        return getattr(self.user, "role", None) in [
            "ADMIN",
            "MANAGER",
        ]

    # ---------------------------------------------------------
    # OFFICE OVERVIEW
    # ---------------------------------------------------------

    def office_overview(self):
        """
        High-level SOMI operational overview.
        """

        employee_count = Employee.objects.count()
        department_count = (
            Employee.objects.values("department")
            .distinct()
            .count()
        )

        attendance_count = Attendance.objects.count()
        leave_count = LeaveRequest.objects.count()
        task_count = Task.objects.count()
        performance_count = PerformanceReview.objects.count()

        completed_tasks = Task.objects.filter(
            status=Task.Status.COMPLETED
        ).count()

        pending_leaves = LeaveRequest.objects.filter(
            status=LeaveRequest.Status.PENDING
        ).count()

        return {
            "employees": employee_count,
            "departments": department_count,
            "attendance_records": attendance_count,
            "leave_requests": leave_count,
            "pending_leaves": pending_leaves,
            "tasks": task_count,
            "completed_tasks": completed_tasks,
            "performance_reviews": performance_count,
        }

    # ---------------------------------------------------------
    # ATTENDANCE INTELLIGENCE
    # ---------------------------------------------------------

    def attendance_intelligence(self, days=30):
        start_date, end_date = self._date_range(days)

        records = Attendance.objects.filter(
            date__range=[start_date, end_date]
        )

        total = records.count()

        present = records.filter(
            status=Attendance.Status.PRESENT
        ).count()

        absent = records.filter(
            status=Attendance.Status.ABSENT
        ).count()

        late = records.filter(
            status=Attendance.Status.LATE
        ).count()

        on_leave = records.filter(
            status=Attendance.Status.ON_LEAVE
        ).count()

        attendance_rate = self._percentage(
            present + late,
            total,
        )

        absence_rate = self._percentage(
            absent,
            total,
        )

        late_rate = self._percentage(
            late,
            total,
        )

        department_breakdown = []

        department_rows = (
            records.values(
                "employee__department__id",
                "employee__department__name",
            )
            .annotate(
                total=Count("id"),
                absent=Count(
                    "id",
                    filter=models_q_absent(),
                ),
                late=Count(
                    "id",
                    filter=models_q_late(),
                ),
            )
            .order_by("-absent", "-late")
        )

        for row in department_rows:
            department_total = row["total"]

            department_breakdown.append(
                {
                    "department_id": row[
                        "employee__department__id"
                    ],
                    "department_name": (
                        row[
                            "employee__department__name"
                        ]
                        or "Unassigned"
                    ),
                    "attendance_records": department_total,
                    "absent": row["absent"],
                    "late": row["late"],
                    "absence_rate": self._percentage(
                        row["absent"],
                        department_total,
                    ),
                    "late_rate": self._percentage(
                        row["late"],
                        department_total,
                    ),
                }
            )

        alerts = []

        if absence_rate >= 15:
            alerts.append(
                {
                    "type": "ATTENDANCE",
                    "severity": "HIGH",
                    "message": (
                        "Absence rate is above the "
                        "normal monitoring threshold."
                    ),
                }
            )

        if late_rate >= 15:
            alerts.append(
                {
                    "type": "ATTENDANCE",
                    "severity": "MEDIUM",
                    "message": (
                        "Late attendance is occurring "
                        "frequently."
                    ),
                }
            )

        return {
            "period": {
                "start": start_date,
                "end": end_date,
                "days": days,
            },
            "total_records": total,
            "present": present,
            "absent": absent,
            "late": late,
            "on_leave": on_leave,
            "attendance_rate": attendance_rate,
            "absence_rate": absence_rate,
            "late_rate": late_rate,
            "department_breakdown": department_breakdown,
            "alerts": alerts,
        }

    # ---------------------------------------------------------
    # LEAVE INTELLIGENCE
    # ---------------------------------------------------------

    def leave_intelligence(self, days=30):
        start_date, end_date = self._date_range(days)

        requests = LeaveRequest.objects.filter(
            request_date__range=[start_date, end_date]
        )

        total = requests.count()

        pending = requests.filter(
            status=LeaveRequest.Status.PENDING
        ).count()

        approved = requests.filter(
            status=LeaveRequest.Status.APPROVED
        ).count()

        rejected = requests.filter(
            status=LeaveRequest.Status.REJECTED
        ).count()

        cancelled = requests.filter(
            status=LeaveRequest.Status.CANCELLED
        ).count()

        total_leave_days = (
            requests.filter(
                status=LeaveRequest.Status.APPROVED
            ).aggregate(
                total=Sum("total_days")
            )["total"]
            or 0
        )

        department_breakdown = []

        department_rows = (
            requests.values(
                "employee__department__id",
                "employee__department__name",
            )
            .annotate(
                requests=Count("id"),
                leave_days=Sum("total_days"),
            )
            .order_by("-leave_days", "-requests")
        )

        for row in department_rows:
            department_breakdown.append(
                {
                    "department_id": row[
                        "employee__department__id"
                    ],
                    "department_name": (
                        row[
                            "employee__department__name"
                        ]
                        or "Unassigned"
                    ),
                    "requests": row["requests"],
                    "leave_days": row["leave_days"] or 0,
                }
            )

        alerts = []

        if pending >= 5:
            alerts.append(
                {
                    "type": "LEAVE",
                    "severity": "MEDIUM",
                    "message": (
                        "Several leave requests are "
                        "currently awaiting review."
                    ),
                }
            )

        if department_breakdown:
            highest = department_breakdown[0]

            if highest["leave_days"] >= 10:
                alerts.append(
                    {
                        "type": "LEAVE",
                        "severity": "MEDIUM",
                        "message": (
                            f'{highest["department_name"]} '
                            "has a relatively high approved "
                            "leave-day concentration."
                        ),
                    }
                )

        return {
            "period": {
                "start": start_date,
                "end": end_date,
                "days": days,
            },
            "total_requests": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "cancelled": cancelled,
            "approved_leave_days": total_leave_days,
            "approval_rate": self._percentage(
                approved,
                total,
            ),
            "department_breakdown": department_breakdown,
            "alerts": alerts,
        }

    # ---------------------------------------------------------
    # TASK INTELLIGENCE
    # ---------------------------------------------------------

    def task_intelligence(self):
        today = timezone.localdate()

        total = Task.objects.count()

        completed = Task.objects.filter(
            status=Task.Status.COMPLETED
        ).count()

        in_progress = Task.objects.filter(
            status=Task.Status.IN_PROGRESS
        ).count()

        review = Task.objects.filter(
            status=Task.Status.REVIEW
        ).count()

        todo = Task.objects.filter(
            status=Task.Status.TODO
        ).count()

        cancelled = Task.objects.filter(
            status=Task.Status.CANCELLED
        ).count()

        overdue = Task.objects.filter(
            due_date__lt=today
        ).exclude(
            status__in=[
                Task.Status.COMPLETED,
                Task.Status.CANCELLED,
            ]
        ).count()

        high_priority_open = Task.objects.filter(
            priority__in=[
                Task.Priority.HIGH,
                Task.Priority.URGENT,
            ]
        ).exclude(
            status__in=[
                Task.Status.COMPLETED,
                Task.Status.CANCELLED,
            ]
        ).count()

        completion_rate = self._percentage(
            completed,
            total,
        )

        workload = []

        employee_rows = (
            Task.objects.values(
                "assigned_to__id",
                "assigned_to__employee_id",
                "assigned_to__user__first_name",
                "assigned_to__user__last_name",
            )
            .annotate(
                total=Count("id"),
                open_tasks=Count(
                    "id",
                    filter=~models_q_completed_cancelled(),
                ),
            )
            .order_by("-open_tasks")
        )

        for row in employee_rows:
            first_name = (
                row[
                    "assigned_to__user__first_name"
                ]
                or ""
            )

            last_name = (
                row[
                    "assigned_to__user__last_name"
                ]
                or ""
            )

            name = (
                f"{first_name} {last_name}"
            ).strip()

            workload.append(
                {
                    "employee_id": row[
                        "assigned_to__id"
                    ],
                    "employee_code": row[
                        "assigned_to__employee_id"
                    ],
                    "employee_name": (
                        name
                        or row[
                            "assigned_to__employee_id"
                        ]
                    ),
                    "total_tasks": row["total"],
                    "open_tasks": row["open_tasks"],
                }
            )

        alerts = []

        if overdue > 0:
            alerts.append(
                {
                    "type": "TASK",
                    "severity": "HIGH",
                    "message": (
                        f"{overdue} task(s) are overdue "
                        "and still open."
                    ),
                }
            )

        if high_priority_open > 0:
            alerts.append(
                {
                    "type": "TASK",
                    "severity": "MEDIUM",
                    "message": (
                        f"{high_priority_open} high-priority "
                        "or urgent task(s) remain open."
                    ),
                }
            )

        return {
            "total": total,
            "completed": completed,
            "in_progress": in_progress,
            "review": review,
            "todo": todo,
            "cancelled": cancelled,
            "overdue": overdue,
            "high_priority_open": high_priority_open,
            "completion_rate": completion_rate,
            "workload": workload,
            "alerts": alerts,
        }

    # ---------------------------------------------------------
    # PERFORMANCE INTELLIGENCE
    # ---------------------------------------------------------

    def performance_intelligence(self):
        reviews = PerformanceReview.objects.all()

        total = reviews.count()

        submitted = reviews.filter(
            status=PerformanceReview.Status.SUBMITTED
        ).count()

        acknowledged = reviews.filter(
            status=PerformanceReview.Status.ACKNOWLEDGED
        ).count()

        draft = reviews.filter(
            status=PerformanceReview.Status.DRAFT
        ).count()

        averages = reviews.aggregate(
            rating=Avg("rating"),
            goals_score=Avg("goals_score"),
            productivity_score=Avg("productivity_score"),
            quality_score=Avg("quality_score"),
            teamwork_score=Avg("teamwork_score"),
            communication_score=Avg(
                "communication_score"
            ),
        )

        department_breakdown = []

        department_rows = (
            reviews.values(
                "employee__department__id",
                "employee__department__name",
            )
            .annotate(
                reviews=Count("id"),
                average_rating=Avg("rating"),
            )
            .order_by("-average_rating")
        )

        for row in department_rows:
            department_breakdown.append(
                {
                    "department_id": row[
                        "employee__department__id"
                    ],
                    "department_name": (
                        row[
                            "employee__department__name"
                        ]
                        or "Unassigned"
                    ),
                    "reviews": row["reviews"],
                    "average_rating": self._decimal_to_float(
                        row["average_rating"]
                    ),
                }
            )

        alerts = []

        if draft > 0:
            alerts.append(
                {
                    "type": "PERFORMANCE",
                    "severity": "MEDIUM",
                    "message": (
                        f"{draft} performance review(s) "
                        "are still in draft status."
                    ),
                }
            )

        return {
            "total_reviews": total,
            "draft": draft,
            "submitted": submitted,
            "acknowledged": acknowledged,
            "average_scores": {
                key: self._decimal_to_float(value)
                for key, value in averages.items()
            },
            "department_breakdown": department_breakdown,
            "alerts": alerts,
        }

    # ---------------------------------------------------------
    # PAYROLL INTELLIGENCE
    # ---------------------------------------------------------

    def payroll_intelligence(self):
        if not self._can_view_payroll():
            return {
                "available": False,
                "message": (
                    "Payroll intelligence is restricted "
                    "to administrators and managers."
                ),
            }

        records = Payroll.objects.all()

        total_records = records.count()

        total_salary = (
            records.aggregate(
                total=Sum("total_salary")
            )["total"]
            or 0
        )

        total_basic = (
            records.aggregate(
                total=Sum("basic_salary")
            )["total"]
            or 0
        )

        total_allowances = (
            records.aggregate(
                total=Sum("other_allowances")
            )["total"]
            or 0
        )

        total_deductions = (
            records.aggregate(
                total=Sum("deductions")
            )["total"]
            or 0
        )

        department_breakdown = []

        department_rows = (
            records.values(
                "employee__department__id",
                "employee__department__name",
            )
            .annotate(
                records=Count("id"),
                payroll_cost=Sum("total_salary"),
            )
            .order_by("-payroll_cost")
        )

        for row in department_rows:
            department_breakdown.append(
                {
                    "department_id": row[
                        "employee__department__id"
                    ],
                    "department_name": (
                        row[
                            "employee__department__name"
                        ]
                        or "Unassigned"
                    ),
                    "records": row["records"],
                    "payroll_cost": self._decimal_to_float(
                        row["payroll_cost"]
                    ),
                }
            )

        return {
            "available": True,
            "total_records": total_records,
            "total_salary": self._decimal_to_float(
                total_salary
            ),
            "basic_salary": self._decimal_to_float(
                total_basic
            ),
            "allowances": self._decimal_to_float(
                total_allowances
            ),
            "deductions": self._decimal_to_float(
                total_deductions
            ),
            "department_breakdown": department_breakdown,
        }

    # ---------------------------------------------------------
    # SMART ALERTS
    # ---------------------------------------------------------

    def smart_alerts(self):
        alerts = []

        attendance = self.attendance_intelligence()
        leave = self.leave_intelligence()
        tasks = self.task_intelligence()
        performance = self.performance_intelligence()

        alerts.extend(attendance["alerts"])
        alerts.extend(leave["alerts"])
        alerts.extend(tasks["alerts"])
        alerts.extend(performance["alerts"])

        return alerts

    # ---------------------------------------------------------
    # COMPLETE INTELLIGENCE SUMMARY
    # ---------------------------------------------------------

    def full_summary(self):
        """
        Complete intelligence payload for the future
        SOMI AI Dashboard and AI Assistant.
        """

        return {
            "generated_at": timezone.now(),
            "overview": self.office_overview(),
            "attendance": self.attendance_intelligence(),
            "leave": self.leave_intelligence(),
            "tasks": self.task_intelligence(),
            "performance": self.performance_intelligence(),
            "payroll": self.payroll_intelligence(),
            "smart_alerts": self.smart_alerts(),
        }


# -------------------------------------------------------------
# QUERY HELPERS
# -------------------------------------------------------------
# Kept here so the engine remains readable while Django's
# conditional Count expressions stay isolated.


def models_q_absent():
    from django.db.models import Q

    return Q(status=Attendance.Status.ABSENT)


def models_q_late():
    from django.db.models import Q

    return Q(status=Attendance.Status.LATE)


def models_q_completed_cancelled():
    from django.db.models import Q

    return Q(
        status__in=[
            Task.Status.COMPLETED,
            Task.Status.CANCELLED,
        ]
    )