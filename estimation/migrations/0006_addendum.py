# Generated by Django 5.1.5 on 2025-02-11 11:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimation', '0005_alter_act_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Addendum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True, verbose_name='Номер додаткової угоди')),
                ('date_signing', models.DateField(verbose_name='Дата підписання')),
                ('description', models.CharField(blank=True, max_length=250, null=True, verbose_name='Примітка')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='addendum', to='estimation.contract', verbose_name='Договір')),
            ],
        ),
    ]
