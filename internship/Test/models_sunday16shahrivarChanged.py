from django.db import models


# from public.models import Users,Teachers,Student,DepartmentHead,FacultyTrainingStaff,UniversityTrainingStaff
from public.models import Users,Student
from public.models import Faculties,College,Major


class InternshipHead(models.Model):
    user  = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    phone = models.CharField(max_length=31)
    email = models.EmailField()



class State(models.Model):
    namestate = models.CharField(max_length=63)
    def __str__(self):
        return self.namestate



class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    namecity  = models.CharField(max_length=63)
    def __str__(self):
        return self.namecity


class InternShipPlace(models.Model):
    nameplace         = models.CharField(max_length=127)
    city              = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    address           = models.TextField()
    phone             = models.CharField(max_length=15)
    internShipWebSite = models.CharField(null=True,blank=True,max_length=127)
    def __str__(self):
        return self.nameplace

Semester = (
    ('1','First Semester'),
    ('2','Second Semester'),
    ('3','Summer'),
)

# class InternshipForm(models.Model):
#     internshipPlace = models.ForeignKey(InternShipPlace,on_delete=models.CASCADE)
#     student         = models.ForeignKey(Student, on_delete=models.CASCADE)
#     term            = models.CharField(choices=Semester, max_length=15)


class Request(models.Model):
    internshipPlace        = models.ForeignKey(InternShipPlace,on_delete=models.CASCADE)
    student                = models.ForeignKey(Student, on_delete=models.CASCADE)
    term                   = models.CharField(choices=Semester, max_length=15)
    # internShipForm         = models.ForeignKey(InternshipForm, on_delete=models.DO_NOTHING, related_name='Rinternshipform')
    title                  = models.CharField(max_length=63)
    comment                = models.TextField(null=True)#text ==>comment
    state                  = models.IntegerField(default=0)
    opinion                = models.BooleanField(default=False)
    agreementUploadedUrl   = models.TextField(null=True)

# States =(
#     ('No Request','State0'),
#     ('Submit Request','State1'),
#     ('FacultyTrainingStaff','State2'),
#     ('DepartmentHead','State3'),
#     ('UniversityTrainingStaff','State4'),
#     ('FacultyTrainingStaff','Role5'),
#     ('UniversityTrainingStaff','Role6'),
#     ('Final Approval','Role7')
# )
#

# class RequestState(models.Model):         ######Combine Request#######
#     request                 = models.OneToOneField(Request, on_delete=models.DO_NOTHING, related_name='RSrequest')
#     state                   = models.IntegerField()


class Opinions(models.Model):
    user         = models.ForeignKey(Users, on_delete=models.DO_NOTHING, related_name='Operson')
    # student      = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name='Ouserstudent')
    # requeststate = models.ForeignKey(RequestState, on_delete=models.DO_NOTHING, related_name='Orequest')
    request      = models.ForeignKey(Request, on_delete=models.DO_NOTHING, related_name='Orequest')
    seenDate     = models.DateTimeField()
    # opinion      = models.BooleanField()
    opinionDate  = models.DateTimeField()
    opinionText  = models.TextField(null=True)


class InternShip(models.Model):
    student                   = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    # internshiphead            = models.ForeignKey(InternshipHead, on_delete=models.DO_NOTHING)
    internshiphead            = models.ForeignKey(InternshipHead, on_delete=models.DO_NOTHING)
    gtOpinion                 = models.ForeignKey(Opinions, on_delete=models.DO_NOTHING)
    guideTeacher              = models.ForeignKey('internship.Choosing', on_delete=models.DO_NOTHING )#choosing
    studentFinalReport        = models.TextField()
    studentObjectionText      = models.TextField()
    studentObjectionDate      = models.DateTimeField()
    supervisorReportUploadUrl = models.TextField()
    internShipState           = models.BooleanField()



class WeeklyConfirmarion(models.Model):
    internship                       = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    weekNumber                       = models.IntegerField()
    supervisorAttendanCeconfirmation = models.BooleanField(default=False)
    supervisorReportConfirmation     = models.BooleanField(default=False)



class AttendanceTable(models.Model):
    # weeklyconfirmarion     = models.ForeignKey(WeeklyConfirmarion, on_delete=models.DO_NOTHING)
    internShip             = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    startTime              = models.DateTimeField()
    endTime                = models.DateTimeField()
    weekNumber             = models.IntegerField()



class WeeklyReport(models.Model):
    internShip                = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    reportDate                = models.DateTimeField()
    weekNumber                = models.IntegerField()
    reportTitle               = models.CharField(max_length=63)
    reportText                = models.TextField()



class Choosing(models.Model):
    user       = models.ForeignKey(Users, on_delete=models.DO_NOTHING)
    student    = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    # departmentHead = models.ForeignKey(DepartmentHead,on_delete=models.DO_NOTHING)
    # GuideTeacher   = models.ForeignKey(Teachers,on_delete=models.DO_NOTHING)
    # internShip = models.ForeignKey(InternShip, on_delete=models.DO_NOTHING)
    gtOpinion  = models.ForeignKey(Opinions, on_delete=models.DO_NOTHING)






class Student_InternShip(models.Model):
    # student             = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    # supervisor          = models.ForeignKey(InternshipHead, on_delete=models.DO_NOTHING)
    # guideTeacher = models.ForeignKey(Teachers,on_delete=models.DO_NOTHING)
    internShip          = models.ForeignKey(InternShip ,on_delete=models.DO_NOTHING)
    gtgrade             = models.FloatField()
    gtgradeconfirmation = models.BooleanField()
