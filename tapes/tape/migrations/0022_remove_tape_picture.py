# Generated by Django 3.2.13 on 2022-06-02 03:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tape', '0021_alter_entry_tape'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tape',
            name='picture',
        ),
    ]
