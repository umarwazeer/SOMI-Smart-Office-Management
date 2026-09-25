from django.db import models


class Payroll(models.Model):

    class PayrollPeriod(models.TextChoices):
        WEEKLY = "WEEKLY", "Weekly"
        BI_WEEKLY = "BI_WEEKLY", "Bi-weekly"
        MONTHLY = "MONTHLY", "Monthly"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
        CHEQUE = "CHEQUE", "Cheque"

    employee = models.ForeignKey(
        "employees.Employee",
        on_delete=models.CASCADE,
        related_name="payroll_records",
    )

    payroll_period = models.CharField(
        max_length=20,
        choices=PayrollPeriod.choices,
        default=PayrollPeriod.MONTHLY,
    )

    basic_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    other_allowances = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    total_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    payment_date = models.DateField()

    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.BANK_TRANSFER,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-payment_date", "-created_at"]

    def __str__(self):
        return (
            f"{self.employee.employee_id} - "
            f"{self.payment_date} - "
            f"{self.total_salary}"
        )