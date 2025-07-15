from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetime import date

def validate_no_future_date(value):
    if value > date.today():
        raise ValidationError("Date of joining cannot be in the future.")

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class Departments(models.Model):
    DepartmentId = models.AutoField(primary_key=True)
    DepartmentName = models.CharField(
        max_length=100,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message="Department name must contain only letters and spaces."
            )
        ]
    )
    is_active = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    # Default manager returns only active records
    objects = ActiveManager()
    # Secondary manager to access all records (including soft-deleted)
    all_objects = models.Manager()

    def __str__(self):
        return self.DepartmentName

    def natural_key(self):
        return (self.DepartmentId, self.DepartmentName)

    class Meta:
        indexes = [
            models.Index(fields=['DepartmentName']),
        ]

class Employees(models.Model):
    EmployeeId = models.AutoField(primary_key=True)
    EmployeeName = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]+$',
                message="Employee name must contain only letters and spaces."
            )
        ]
    )
    Email = models.EmailField(unique=True, blank=True, null=True)
    Department = models.ForeignKey(
        Departments,
        to_field='DepartmentId',
        on_delete=models.CASCADE,
        related_name='employees'
    )
    DateOfJoining = models.DateField(validators=[validate_no_future_date])
    PhotoFileName = models.CharField(max_length=100, blank=True, null=True, default='default.png')
    is_active = models.BooleanField(default=True)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    # Default manager returns only active records
    objects = ActiveManager()
    # Secondary manager to access all records (including soft-deleted)
    all_objects = models.Manager()

    def __str__(self):
        return self.EmployeeName

    class Meta:
        indexes = [
            models.Index(fields=['EmployeeName']),
            models.Index(fields=['Department']),
        ]