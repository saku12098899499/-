# Generated by Django 4.1.1 on 2022-11-25 08:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_alter_request_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='reward',
            field=models.DecimalField(decimal_places=3, default=0.001, max_digits=5, validators=[django.core.validators.MinValueValidator(0.001), django.core.validators.MaxValueValidator(10.0)], verbose_name='報酬'),
        ),
    ]
