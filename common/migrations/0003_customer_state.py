# Generated by Django 5.1.7 on 2025-03-15 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_customer_qq'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='state',
            field=models.BooleanField(default=True),
        ),
    ]
