# Generated by Django 4.2.2 on 2023-07-11 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0018_alter_leavetracker_available_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavetracker',
            name='Available_Days',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
