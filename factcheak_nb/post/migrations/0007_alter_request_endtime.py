# Generated by Django 4.1.1 on 2022-11-21 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_alter_request_reward'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='endtime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
