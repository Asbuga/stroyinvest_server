from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver

ROLES = ["admin", "department_head", "employee"]

PERMISSIONS  = [
    ("add_department", "Can add department"),
    ("change_department", "Can change department"),
    ("delete_department", "Can delete department"),
    ("view_department", "Can view department"),
    ("add_position", "Can add position"),
    ("change_position", "Can change position"),
    ("delete_position", "Can delete position"),
    ("view_position", "Can view position"),
    ("add_employee", "Can add employee"),
    ("change_employee", "Can change employee"),
    ("delete_employee", "Can delete employee"),
    ("view_employee", "Can view employee"),
]


@receiver(post_migrate)
def create_role(sender, *args, **kwargs):
    if sender.name == "users":
        for role in ROLES:
            Group.objects.get_or_create(name=role)


@receiver(post_migrate)
def create_permissions(sender, *args, **kwargs):
    if sender.name == "users":
        for codename, name in PERMISSIONS:
            Permission.objects.get_or_create(codename=codename, name=name)

        admin = Group.objects.get(name="admin")
        department_head = Group.objects.get(name="department_head")
        employee = Group.objects.get(name="employee")

        admin.permissions.set(Permission.objects.all())
        
        department_head.permissions.set(
            Permission.objects.filter(
                codename__in=["view_department", "view_position", "view_employee"]
            )
        )
        
        employee.permissions.set(
            Permission.objects.filter(
                codename__in=["view_department", "view_position", "view_employee"]
            )
        )
