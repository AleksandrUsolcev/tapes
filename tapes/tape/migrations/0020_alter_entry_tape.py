# Generated by Django 3.2.13 on 2022-05-30 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tape', '0019_alter_tape_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tape',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='tape.tape', verbose_name='Лента'),
        ),
    ]
