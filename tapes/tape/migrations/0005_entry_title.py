# Generated by Django 3.2.13 on 2022-05-21 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tape', '0004_auto_20220521_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Заголовок'),
        ),
    ]
