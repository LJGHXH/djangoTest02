# Generated by Django 5.1.7 on 2025-03-22 03:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_country_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='students', to='common.country'),
        ),
    ]
