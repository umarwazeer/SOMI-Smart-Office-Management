from django.db import models


class PerformanceReview(models.Model):
    class ReviewPeriod(models.TextChoices):
        MONTHLY = "MONTHLY", "Monthly"
        QUARTERLY = "QUARTERLY", "Quarterly"
        HALF_YEARLY = "HALF_YEARLY", "Half-Yearly"
        YEARLY = "YEARLY", "Yearly"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        SUBMITTED = "SUBMITTED", "Submitted"
        ACKNOWLEDGED = "ACKNOWLEDGED", "Acknowledged"

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="performance_reviews",
    )

    review_period = models.CharField(
        max_length=20,
        choices=ReviewPeriod.choices,
        default=ReviewPeriod.QUARTERLY,
    )

    review_date = models.DateField()

    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    goals_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    productivity_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    quality_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    teamwork_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    communication_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
    )

    strengths = models.TextField(
        blank=True,
        null=True,
    )

    improvement_areas = models.TextField(
        blank=True,
        null=True,
    )

    manager_feedback = models.TextField(
        blank=True,
        null=True,
    )

    employee_comments = models.TextField(
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-review_date", "-created_at"]

    def __str__(self):
        return f"{self.employee} - {self.review_period} - {self.review_date}"