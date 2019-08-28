# Generated by Django 2.2.4 on 2019-08-28 06:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('public', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='InternShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentFinalReport', models.TextField()),
                ('studentObjectionText', models.TextField()),
                ('studentObjectionDate', models.DateTimeField()),
                ('supervisorReportUploadUrl', models.TextField()),
                ('supervisorEmail', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='InternshipForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('internShipWebSite', models.CharField(max_length=127)),
                ('term', models.CharField(max_length=4)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.City')),
            ],
        ),
        migrations.CreateModel(
            name='InternshipHead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
                ('phone', models.CharField(max_length=31)),
                ('email', models.EmailField(max_length=254)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='InternShipPlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=127)),
            ],
        ),
        migrations.CreateModel(
            name='InternShipState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31)),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63)),
                ('text', models.TextField()),
                ('internShipConfirmation', models.IntegerField()),
                ('agreementUploadedUrl', models.TextField()),
                ('internShipForm', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Rinternshipform', to='internship.InternshipForm')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Rstudent', to='public.Student')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63)),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reportDate', models.DateTimeField()),
                ('weekNumber', models.IntegerField()),
                ('reportTitle', models.CharField(max_length=63)),
                ('reportAttachmentUploadUrl', models.TextField()),
                ('reportText', models.TextField()),
                ('supervisorConfirmation', models.BooleanField()),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
            ],
        ),
        migrations.CreateModel(
            name='Student_InternShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guideTeacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Teachers')),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternshipHead')),
            ],
        ),
        migrations.CreateModel(
            name='RequestState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.BooleanField()),
                ('departmentHead', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSrequestdepartmenthead', to='public.DepartmentHead')),
                ('facultyTrainingStaff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSrequestfacultytrainingstaff', to='public.FacultyTrainingStaff')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSrequest', to='internship.Request')),
                ('universityTrainingStaff', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='RSrequestuniversitysrainingstaff', to='public.UniversityTrainingStaff')),
            ],
        ),
        migrations.CreateModel(
            name='Opinions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seenDate', models.DateTimeField()),
                ('opinion', models.TextField()),
                ('opinionDate', models.DateTimeField()),
                ('opinionText', models.TextField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Operson', to=settings.AUTH_USER_MODEL)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Orequest', to='internship.Request')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='Ouserstudent', to='public.Student')),
            ],
        ),
        migrations.AddField(
            model_name='internshipform',
            name='internShipPlace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShipPlace'),
        ),
        migrations.AddField(
            model_name='internshipform',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.State'),
        ),
        migrations.AddField(
            model_name='internshipform',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='public.Student'),
        ),
        migrations.AddField(
            model_name='internship',
            name='gtOpinion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.Opinions'),
        ),
        migrations.AddField(
            model_name='internship',
            name='internShipState',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShipState'),
        ),
        migrations.CreateModel(
            name='Choosing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('GTOpinion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.Opinions')),
                ('GuideTeacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Teachers')),
                ('departmentHead', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.DepartmentHead')),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='public.Student')),
            ],
        ),
        migrations.CreateModel(
            name='AttendanceTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('supervisorConfirmation', models.BooleanField()),
                ('internShip', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='internship.InternShip')),
            ],
        ),
    ]
