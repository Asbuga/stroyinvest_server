# Generated by Django 5.1.5 on 2025-02-11 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimation', '0007_contract_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='status',
            field=models.BooleanField(choices=[(True, 'Активний'), (False, 'Завершений')], max_length=21, verbose_name='Статус договору'),
        ),
    ]
