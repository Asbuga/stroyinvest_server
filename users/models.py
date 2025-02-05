from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Employee(models.Model):
    ROLE = [
        ("director", "Генеральний директор"),
        ("deputy_director", "Заступник директора"),

        ("manager", "Менеджер"),
        ("foreman", "Прораб"),

        ("chief_estimator", "Начальник кошторисного відділу"),
        ("estimator", "Кошторисник"),

        ("chief_accountant", "Головний бухгалтер"),
        ("accountant", "Бухгалтер"),

        ("chief_engineer", "Головний інженер"),
        ("engineer", "Інженер ПТО"),

        ("chief_economist", "Головний економіст"),
        ("economist", "Економіст"),

        ("chief_lawyer", "Головний юрист"),
        ("lawyer", "Юрист"),

        ("chief_supply", "Начальник відділу постачання"),
        ("supply_specialist", "Фахівець відділу постачання"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Працівник")
    role = models.CharField(max_length=30, choices=ROLE, verbose_name="Посада")
    birthday = models.DateField(verbose_name="День народження")
    mobile_phone = models.CharField(
        max_length=13,
        unique=True,
        verbose_name="Номер мобільного телефону",
        validators=[
            RegexValidator(r"^+\d{12}$", "Введіть номер телефону з +38..")
        ],
    )
    internal_phone = models.CharField(
        max_length=3,
        verbose_name="Номер внутрішнього телефону",
        validators=[
            RegexValidator(r"^\d{3}$", "Введіть номер внутрішнього телефону.")
        ],
    )

    class Meta:
        verbose_name_plural = "employees"

    def __str__(self):
        return f"{self.role} - {self.user.first_name} {self.user.last_name}"
