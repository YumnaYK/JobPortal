# Generated by Django 4.2.2 on 2023-07-11 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0014_leavetracker_available_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leavetracker',
            name='Available_Days',
        ),
    ]
