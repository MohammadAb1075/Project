# Generated by Django 2.2.4 on 2019-09-05 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_auto_20190903_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='average',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='credits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]