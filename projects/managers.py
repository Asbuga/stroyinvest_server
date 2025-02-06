from django.db import models

from users.models import Employee


class ProjectManager(models.Manager):
    def get_estimator_projects(self, user):
        try:
            employee = Employee.objects.get(user=user)  
            return self.filter(estimator=employee)  
        except Employee.DoesNotExist:
            return self.none()
