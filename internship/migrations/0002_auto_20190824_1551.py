# Generated by Django 2.2.4 on 2019-08-24 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='departmenthead',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='facultytrainingstaff',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='universitytrainingstaff',
            old_name='first_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='departmenthead',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='facultytrainingstaff',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='universitytrainingstaff',
            name='last_name',
        ),
    ]