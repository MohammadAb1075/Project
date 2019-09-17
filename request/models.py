from django.db import models
from public.models import Student
from public.models import Users
# Create your models here.


class ApprovementStatePath(models.Model):
    statesPath = models.CharField(max_length=15)


class RequestType(models.Model):
    name = models.CharField(max_length=63)
    approvementStatePath = models.ForeignKey(ApprovementStatePath,on_delete=models.DO_NOTHING)


class StatePath(models.Model):
    approvementStatePath = models.ForeignKey(ApprovementStatePath,on_delete=models.DO_NOTHING)
    preState = models.IntegerField()
    state = models.IntegerField()





class Request(models.Model):
    requestType = models.ForeignKey(RequestType,on_delete=models.DO_NOTHING)
    applicant = models.ForeignKey(Student,related_name='Student',on_delete=models.DO_NOTHING)
    consideration = models.TextField()
    modificationDate = models.DateTimeField()
    isEnded = models.BooleanField()


class Agreement(models.Model):
    request = models.ForeignKey(Request,on_delete=models.DO_NOTHING)
    state = models.ForeignKey(StatePath,on_delete=models.DO_NOTHING)
    comment = models.TextField()
    acceptance = models.BooleanField(default=False)


Choices = (

    ('1','seen'),
    ('2','commented')
)



class Comments(models.Model):
    request = models.ForeignKey(Request,on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Users,on_delete=models.DO_NOTHING)
    state = models.ForeignKey(Agreement,on_delete=models.DO_NOTHING)
    typeComment = models.CharField(choices=Choices, max_length=2)
    date = models.DateTimeField()


class Files(models.Model):
    request = models.ForeignKey(Request,on_delete=models.DO_NOTHING)
    file = models.FileField()
    state = models.ForeignKey(StatePath,on_delete=models.DO_NOTHING)



class Instatation(models.Model):
    request = models.ForeignKey(Request,on_delete=models.DO_NOTHING)



class setArchieve(models.Model):
    setter = models.ForeignKey(Users,on_delete=models.DO_NOTHING)
    request = models.ForeignKey(Request,on_delete=models.DO_NOTHING)


class setStarred(models.Model):
    setter = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    request = models.ForeignKey(Request, on_delete=models.DO_NOTHING)


