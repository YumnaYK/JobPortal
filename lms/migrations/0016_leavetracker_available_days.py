# Generated by Django 4.2.2 on 2023-07-11 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0015_remove_leavetracker_available_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavetracker',
            name='Available_Days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
