# Generated by Django 3.2.13 on 2022-05-24 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=None, max_length=32, unique=True),
            preserve_default=False,
        ),
    ]
