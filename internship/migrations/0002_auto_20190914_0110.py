# Generated by Django 2.2.4 on 2019-09-13 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='term',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3')], max_length=15),
        ),
    ]