# Generated by Django 3.2.15 on 2022-08-19 04:49

from django.db import migrations, models
import django.utils.timezone
import django_quill.fields
import users.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', users.fields.LowercaseEmailField(max_length=254, unique=True, verbose_name='email address')),
                ('username', users.fields.LowercaseSlugField(max_length=24, unique=True, verbose_name='Имя пользователя')),
                ('about', django_quill.fields.QuillField(blank=True, null=True)),
                ('display_username', models.CharField(blank=True, max_length=24, null=True)),
                ('full_name', models.CharField(blank=True, max_length=48, null=True)),
                ('show_full_name', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_newbie', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('avatar', models.ImageField(blank=True, upload_to='user-avatars/')),
                ('background', models.ImageField(blank=True, upload_to='user-backgrounds/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
    ]
