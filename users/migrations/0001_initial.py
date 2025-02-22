# Generated by Django 5.1.5 on 2025-02-06 08:32

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Найменування відділу')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Найменування посади')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Короткий опис посади')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.department', verbose_name='Найменування відділу')),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birth_day', models.DateField(verbose_name='День народження')),
                ('mobile_phone', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator('^+\\d{12}$', 'Введіть номер телефону з +38..')], verbose_name='Номер мобільного телефону')),
                ('internal_phone', models.CharField(blank=True, max_length=3, null=True, validators=[django.core.validators.RegexValidator('^\\d{3}$', 'Введіть номер внутрішнього телефону.')], verbose_name='Номер внутрішнього телефону')),
                ('create_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата створення')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department', verbose_name='Відділ')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Працівник')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.position', verbose_name='Посада')),
            ],
        ),
    ]
