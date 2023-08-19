# Generated by Django 4.2.2 on 2023-07-03 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.CharField(blank=True, max_length=25, null=True)),
                ('designation', models.CharField(blank=True, max_length=25, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('leave_balance', models.IntegerField(blank=True, default=0, null=True)),
                ('total_remaining_leaves', models.IntegerField(blank=True, null=True)),
                ('reports_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.employeedetails')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]