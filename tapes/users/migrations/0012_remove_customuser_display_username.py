# Generated by Django 3.2.13 on 2022-05-25 04:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_customuser_display_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='display_username',
        ),
    ]