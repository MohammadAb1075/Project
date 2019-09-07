from django.db import models
from django.contrib.auth.models import AbstractUser


class Users(AbstractUser):
    roles = models.ManyToManyField('public.Role')

    def __str__(self):
        return self.first_name + ' ' + self.last_name



Roles = (
    # ('User','Role1'),
    ('Student','Role1'),
    ('Teacher','Role2'),
    ('DepartmentHead','Role3'),
    ('FacultyTrainingStaff','Role4'),
    ('UniversityTrainingStaff','Role5'),
    ('InternshipHead','Role6')
)


class Role(models.Model):
    role = models.CharField(choices=Roles,max_length=31)

    def __str__(self):
        return self.role


class Student(models.Model):
    user           = models.ForeignKey(Users, on_delete=models.CASCADE)
    major          = models.ForeignKey('public.Major', on_delete=models.CASCADE)
    credits        = models.IntegerField()
    average        = models.FloatField()
    studentNumber  = models.CharField(max_length=9)
    phone          = models.CharField(max_length=11)
    nationalCode   = models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name



class College(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Faculties(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Major(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name    = models.CharField(max_length=63)

    def __str__(self):
        return self.name
