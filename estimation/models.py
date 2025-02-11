from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from .managers import ContractManagers
from projects.models import Project


class Company(models.Model):
    name = models.CharField(
        max_length=250, unique=True, verbose_name="Повне найменування організації"
    )
    edrpou = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="ЄДРПОУ",
        validators=[RegexValidator(r"^\d{8}$", "ЄДРПОУ повинен містити рівно 8 цифр.")],
    )

    class Meta:
        verbose_name_plural = "companies"

    def __str__(self):
        return f"{self.name}"


class Contract(models.Model):
    CONTRACT_NAME = [
        ("Замовник", "Замовник"),
        ("Підрядник", "Підрядник"),
        ("Виконавець", "Виконавець"),
        ("Генпідрядник", "Генпідрядник"),
        ("Генеральний підрядник", "Генеральний підрядник"),
        ("Субпідрядник", "Субпідрядник"),
    ]
    CONTRACT_TYPE = [
        ("ГП", "Генпідрядний"),
        ("СП", "Субпідрядний"),
    ]
    number = models.CharField(
        max_length=15, unique=True, verbose_name="Номер договору №:"
    )
    date_signing = models.DateField(verbose_name="Дата підписання договору")
    date_completion = models.DateField(verbose_name="Дата завершеня договору")
    customer = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="contracts_as_customer",
        verbose_name="Замовник",
    )
    customer_contract_name = models.CharField(
        max_length=21,
        choices=CONTRACT_NAME,
        verbose_name="Найменування Замовника за договором",
    )
    contractor = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name="contracts_as_contractor",
        verbose_name="Підрядник",
    )
    contractor_contract_name = models.CharField(
        max_length=21,
        choices=CONTRACT_NAME,
        verbose_name="Найменування Підрядника за договором",
    )
    summ = models.DecimalField(
        max_digits=11, decimal_places=2, verbose_name="Сума договору"
    )
    subject_contract = models.CharField(
        max_length=1500, verbose_name="Предмет договору"
    )
    shot_subject_contract = models.ForeignKey(
        Project, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Назва проекту"
    )
    address = models.CharField(max_length=300, blank=True, null=True, verbose_name="Адреса об`єкту")
    type = models.CharField(
        max_length=15, choices=CONTRACT_TYPE, default="ГП", verbose_name="Тип договору"
    )
    status = models.BooleanField(
        default=True,
        choices=[
            (True, "Активний"),
            (False, "Завершений")
        ],
        verbose_name="Статус договору",
    )

    objects = ContractManagers()

    class Meta:
        verbose_name_plural = "contracts"

    def __str__(self):
        return f"{self.shot_subject_contract} - Договір №{self.number} від {self.date_signing} на суму {self.summ}"

    def clean(self):
        if self.customer == self.contractor:
            raise ValidationError(
                "Замовник і підрядник не можуть бути однією компанією."
            )
    
    def get_status(self):
        return self.get_status_display()


class Act(models.Model):
    MONTHS = [
        ("Січень", "Січень"),
        ("Лютий", "Лютий"),
        ("Березень", "Березень"),
        ("Квітень", "Квітень"),
        ("Травень", "Травень"),
        ("Червень", "Червень"),
        ("Липень", "Липень"),
        ("Серпень", "Серпень"),
        ("Вересень", "Вересень"),
        ("Жовтень", "Жовтень"),
        ("Листопад", "Листопад"),
        ("Грудень", "Грудень"),
    ]
    contract = models.ForeignKey(
        Contract, on_delete=models.PROTECT, related_name="acts", verbose_name="Договір"
    )
    period = models.CharField(
        max_length=15, choices=MONTHS, verbose_name="Період будівництва"
    )
    year = models.IntegerField(
        verbose_name="Рік",
        validators=[MinValueValidator(2021), MaxValueValidator(2030)],
    )
    number = models.IntegerField(
        verbose_name="Номер акту",
        validators=[MinValueValidator(1), MaxValueValidator(200)],
    )
    date = models.DateField(blank=True, null=True, verbose_name="Дата підписання акту")
    summ = models.DecimalField(
        max_digits=11, decimal_places=2, verbose_name="Сума акту"
    )
    salary = models.DecimalField(
        max_digits=11, decimal_places=2, verbose_name="Заробітна плата в акті"
    )
    man_hours = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Трудовитрати"
    )
    description = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Примітка до акту"
    )

    class Meta:
        verbose_name = "act"
        verbose_name_plural = "acts"

    def __str__(self):
        return f"{self.contract} - Акт № {self.number} за {self.date} на суму {self.summ} грн."


class Addendum(models.Model):
    """Клас описує додаткові угоди до договору."""
    contract = models.ForeignKey(
        Contract, on_delete=models.PROTECT, related_name="addendum", verbose_name="Договір"
    )
    number = models.CharField(
        max_length=10, unique=True, verbose_name="Номер додаткової угоди"
    )
    date_signing = models.DateField(verbose_name="Дата підписання")
    description = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Примітка"
    )
