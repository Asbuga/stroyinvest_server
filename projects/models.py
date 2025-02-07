from django.db import models

from users.models import Employee
from .managers import ProjectManager


class Project(models.Model):
    name = models.CharField(
        max_length=256, unique=True, verbose_name="Коротка назва проекту"
    )
    manager = models.ForeignKey(
        Employee,
        related_name="managed_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    engineer = models.ForeignKey(
        Employee,
        related_name="engineer_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    foreman = models.ForeignKey(
        Employee,
        related_name="foreman_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    estimator = models.ForeignKey(
        Employee,
        related_name="estimator_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    supply = models.ForeignKey(
        Employee,
        related_name="supply_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    accountant = models.ForeignKey(
        Employee,
        related_name="accountant_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    economist = models.ForeignKey(
        Employee,
        related_name="economist_projects",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    objects = ProjectManager()

    def __str__(self):
        return self.name
