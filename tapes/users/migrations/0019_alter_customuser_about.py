# Generated by Django 3.2.13 on 2022-05-29 13:51

from django.db import migrations
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_customuser_background'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='about',
            field=django_quill.fields.QuillField(default=''),
            preserve_default=False,
        ),
    ]
