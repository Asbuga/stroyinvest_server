# Generated by Django 5.1.5 on 2025-02-03 12:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimation', '0003_remove_contract_contractor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='act',
            name='year',
            field=models.IntegerField(default=2024, validators=[django.core.validators.MinValueValidator(2021), django.core.validators.MaxValueValidator(2030)], verbose_name='Рік'),
            preserve_default=False,
        ),
    ]
