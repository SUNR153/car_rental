# Generated by Django 5.1.7 on 2025-04-21 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_password_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='language',
            field=models.CharField(choices=[('ru', 'Русский'), ('en', 'English'), ('kz', 'Қазақша')], default='ru', max_length=10),
        ),
        migrations.AddField(
            model_name='profile',
            name='theme',
            field=models.CharField(choices=[('light', 'Светлая'), ('dark', 'Тёмная')], default='light', max_length=20),
        ),
    ]
