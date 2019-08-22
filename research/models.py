from django.db import models
from django.contrib.auth.models import User


class Faculties(models.Model):
    name = models.CharField(max_length=255)


class Department(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)


class Institute(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)


class College(models.Model):
    faculty = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)



Items=(
    ('1', 'accepted'),
    ('2', 'rejected'),
    ('3', 'unverified')
)

class Programs(models.Model):

    faculty                     = models.ForeignKey(Faculties, on_delete=models.CASCADE)
    Institute                   = models.ForeignKey(Institute, on_delete=models.CASCADE)
    college                     = models.ForeignKey(College, on_delete=models.CASCADE)
    departmentSignatureApproval = models.ForeignKey(User, on_delete=models.DO_NOTHING ,related_name='Progdepartmentsignatureapproval')
    facultySignatureApproval    = models.ForeignKey(User, on_delete=models.DO_NOTHING ,related_name='Progfacultysignatureapproval')
    collegeSignatureApproval    = models.ForeignKey(User, on_delete=models.DO_NOTHING ,related_name='Progcollegesignatureapproval')
    universitySignatureApproval = models.ForeignKey(User, on_delete=models.DO_NOTHING ,related_name='Proguniversitysignatureapproval')
    faTitle                     = models.TextField()
    enTitle                     = models.TextField()
    timeRunMonth                = models.IntegerField()
    dateSuggestion              = models.IntegerField()
    goals                       = models.TextField()
    reason                      = models.TextField()
    interdisciplinary           = models.TextField()
    departmentGoals             = models.CharField(max_length=63)
    departmentApproval          = models.CharField(choices=Items, max_length=2)
    departmentDateApproval      = models.DateTimeField(auto_now_add=True)
    facultyApproval             = models.CharField(choices=Items, max_length=2)
    facultyDateApproval         = models.DateTimeField(auto_now_add=True)
    collegeApproval             = models.CharField(choices=Items, max_length=2)
    collegeDateApproval         = models.DateTimeField(auto_now_add=True)
    universityApproval          = models.CharField(choices=Items, max_length=2)
    universityDateApproval      = models.DateTimeField(auto_now_add=True)



class Major(models.Model):
    name = models.CharField(max_length=63)


class Location(models.Model):
    name = models.CharField(max_length=63)


class Enforcers(models.Model):
    field           = models.ForeignKey(Major, on_delete=models.DO_NOTHING)
    serviceLocation = models.ForeignKey(Location, on_delete=models.DO_NOTHING)
    teamID          = models.IntegerField()
    fullName        = models.CharField(max_length=127)
    rank            = models.IntegerField()
    dutyDescribtion = models.TextField()
    workPhone       = models.CharField(max_length=31)
    mobile          = models.CharField(max_length=31)
    email           = models.EmailField()


class CorrespondingMember(models.Model):
    program   = models.ForeignKey(Programs, on_delete=models.CASCADE)
    enforcers = models.ForeignKey(Enforcers, on_delete=models.DO_NOTHING)
    task      = models.TextField()


class Scheduling(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.DO_NOTHING)
    row     = models.IntegerField()
    title   = models.TextField()
    start   = models.IntegerField()
    end     = models.IntegerField()


class Expected(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.DO_NOTHING)
    type    = models.TextField()


class Attachments(models.Model):
    program = models.ForeignKey(Programs, on_delete=models.CASCADE)
    file    = models.FileField()