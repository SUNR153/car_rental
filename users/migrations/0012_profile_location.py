# Generated by Django 5.1.7 on 2025-05-01 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_profile_preferred_map'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
