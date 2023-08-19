# Generated by Django 4.2.2 on 2023-07-05 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0005_leavetype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='status',
            field=models.CharField(choices=[('approved', 'approved'), ('pending', 'pending'), ('rejected', 'rejected')], default='pending', max_length=8),
        ),
    ]