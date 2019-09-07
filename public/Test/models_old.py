from django.db import models
from django.contrib.auth.models import AbstractUser

#
# Roles = (
#     ('User','Role1'),
#     ('Student','Role2'),
#     ('Teacher','Role3'),
#     ('DepartmentHead','Role4'),
#     ('FacultyTrainingStaff','Role5'),
#     ('UniversityTrainingStaff','Role6'),
#     ('InternshipHead','Role7')
# )

class Users(AbstractUser):
    # role = models.CharField(choices = Roles, max_length = 63)
    # role = models.ForeignKey('public.Role', on_delete=models.DO_NOTHING)
    role = models.ManyToManyField('public.Role')

    def __str__(self):
        return self.first_name + ' ' + self.last_name



Roles = (
    # ('User','Role1'),
    ('Student','Role2'),
    ('Teacher','Role3'),
    ('DepartmentHead','Role4'),
    ('FacultyTrainingStaff','Role5'),
    ('UniversityTrainingStaff','Role6'),
    ('InternshipHead','Role7')
)

class Role(models.Model):
    role = models.CharField(choices=Roles,max_length=31)

    def __str__(self):
        return self.role


class Student(models.Model):
    user           = models.ForeignKey(Users, on_delete=models.CASCADE)
    # college        = models.ForeignKey('public.College', on_delete=models.DO_NOTHING)
    # faculty        = models.ForeignKey('public.Faculties', on_delete=models.DO_NOTHING)
    major          = models.ForeignKey('public.Major', on_delete=models.CASCADE)
    credits        = models.IntegerField()
    average        = models.FloatField()
    studentNumber  = models.CharField(max_length=9)
    phone          = models.CharField(max_length=11)
    nationalCode   = models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name


# class Teachers(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.first_name + ' ' + self.user.last_name
#
#
# class DepartmentHead(models.Model):
#     user       = models.ForeignKey(Users, on_delete=models.CASCADE)
#     department = models.OneToOneField('public.Department', on_delete=models.CASCADE)
#
#
#
#
#     def __str__(self):
#         return self.user.first_name + ' ' + self.user.last_name
#
#
# class FacultyTrainingStaff(models.Model):
#     user    = models.ForeignKey(Users, on_delete=models.CASCADE)
#     faculty = models.OneToOneField('public.Faculties', on_delete=models.CASCADE)
#
#
#     def __str__(self):
#         return self.user.first_name + ' ' + self.user.last_name
#
#
# class UniversityTrainingStaff(models.Model):
#     user    = models.ForeignKey(Users, on_delete=models.CASCADE)
#     college = models.OneToOneField('public.College', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.user.first_name + ' ' + self.user.last_name


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


# class Institute(models.Model):
#     faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
#     name    = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.name

class Major(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name    = models.CharField(max_length=63)

    def __str__(self):
        return self.name
