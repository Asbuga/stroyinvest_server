from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils.timezone import now


class Department(models.Model):
    title = models.CharField(
        max_length=100, unique=True, verbose_name="Відділ"
    )
    create_at = models.DateTimeField(default=now, verbose_name="Дата створення")

    def __str__(self):
        return self.title


class Position(models.Model):
    title = models.CharField(
        max_length=200, unique=True, verbose_name="Посада"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, verbose_name="Відділ"
    )
    description = models.TextField(
        max_length=500, blank=True, null=True, verbose_name="Короткий опис посади", help_text="не обов`язково"
    )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return self.title


class Employee(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Працівник"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, verbose_name="Відділ"
    )
    position = models.ForeignKey(
        Position, on_delete=models.PROTECT, verbose_name="Посада"
    )
    birth_day = models.DateField(verbose_name="День народження")
    mobile_phone = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="Номер мобільного телефону",
        validators=[RegexValidator(r"^\+\d{12}$", "Введіть номер телефону з +38..")],
    )
    internal_phone = models.CharField(
        max_length=3,
        null=True,
        blank=True,
        verbose_name="Номер внутрішнього телефону",
        validators=[RegexValidator(r"^\d{3}$", "Введіть номер внутрішнього телефону.")],
    )
    create_at = models.DateTimeField(default=now, verbose_name="Дата створення")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
