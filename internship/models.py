from django.db import models
from public.models import Users,Teachers,Student,DepartmentHead,FacultyTrainingStaff,UniversityTrainingStaff
from public.models import Faculties,College,Major


class InternshipHead(models.Model):
    user    = models.ForeignKey(Users, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    name    = models.CharField(max_length=31)
    phone   = models.CharField(max_length=31)
    email   = models.EmailField()


class State(models.Model):
    name = models.CharField(max_length=63)


class City(models.Model):
    name = models.CharField(max_length=63)


class InternShipPlace(models.Model):
    name = models.CharField(max_length=127)


class InternshipForm(models.Model):
    student           = models.ForeignKey(Student, on_delete=models.CASCADE)
    # internShipPlace   = models.ForeignKey(InternShipPlace, on_delete=models.DO_NOTHING)
    state             = models.ForeignKey(State, on_delete=models.DO_NOTHING)
    city              = models.ForeignKey(City, on_delete=models.DO_NOTHING)
    # state             = models.CharField(max_length=63)
    # city              = models.CharField(max_length=63)
    internShipPlace   = models.CharField(max_length=127)
    phone             = models.CharField(max_length=15)
    address           = models.TextField()
    internShipWebSite = models.CharField(max_length=127)
    term              = models.CharField(max_length=4)



class Request(models.Model):
    student                = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name='Rstudent')
    internShipForm         = models.ForeignKey(InternshipForm, on_delete=models.DO_NOTHING, related_name='Rinternshipform')
    title                  = models.CharField(max_length=63)
    text                   = models.TextField()
    internShipConfirmation = models.IntegerField()
    agreementUploadedUrl   = models.TextField()


class InternShipState(models.Model):
    name = models.CharField(max_length=31)


class RequestState(models.Model):
    request                 = models.ForeignKey(Request, on_delete=models.DO_NOTHING, related_name='RSrequest')
    facultyTrainingStaff    = models.ForeignKey(FacultyTrainingStaff, on_delete=models.DO_NOTHING, related_name='RSrequestfacultytrainingstaff')
    universityTrainingStaff = models.ForeignKey(UniversityTrainingStaff, on_delete=models.DO_NOTHING, related_name='RSrequestuniversitysrainingstaff')
    departmentHead          = models.ForeignKey(DepartmentHead, on_delete=models.DO_NOTHING, related_name='RSrequestdepartmenthead')
    state                   = models.BooleanField()


class Opinions(models.Model):
    person      = models.ForeignKey(Users, on_delete=models.DO_NOTHING, related_name='Operson')
    student     = models.ForeignKey(Student, on_delete=models.DO_NOTHING, related_name='Ouserstudent')
    request     = models.ForeignKey(Request, on_delete=models.DO_NOTHING, related_name='Orequest')
    seenDate    = models.DateTimeField()
    opinion     = models.TextField()
    opinionDate = models.DateTimeField()
    opinionText = models.TextField()




class InternShip(models.Model):
    internShipState           = models.ForeignKey(InternShipState,on_delete=models.DO_NOTHING)
    gtOpinion                 = models.ForeignKey(Opinions,on_delete=models.DO_NOTHING)
    studentFinalReport        = models.TextField()
    studentObjectionText      = models.TextField()
    studentObjectionDate      = models.DateTimeField()
    supervisorReportUploadUrl = models.TextField()
    supervisorEmail           = models.EmailField()





class AttendanceTable(models.Model):
    internShip             = models.ForeignKey(InternShip,on_delete=models.DO_NOTHING)
    startTime              = models.DateTimeField()
    endTime                = models.DateTimeField()
    supervisorConfirmation = models.BooleanField()



class WeeklyReport(models.Model):
    internShip                = models.ForeignKey(InternShip,on_delete=models.DO_NOTHING)
    reportDate                = models.DateTimeField()
    weekNumber                = models.IntegerField()
    reportTitle               = models.CharField(max_length=63)
    reportAttachmentUploadUrl = models.TextField()
    reportText                = models.TextField()
    supervisorConfirmation    = models.BooleanField()



class Choosing(models.Model):
    student        = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    departmentHead = models.ForeignKey(DepartmentHead,on_delete=models.DO_NOTHING)
    GuideTeacher   = models.ForeignKey(Teachers,on_delete=models.DO_NOTHING)
    internShip     = models.ForeignKey(InternShip,on_delete=models.DO_NOTHING)
    GTOpinion      = models.ForeignKey(Opinions,on_delete=models.DO_NOTHING)



class Student_InternShip(models.Model):
    student      = models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    supervisor   = models.ForeignKey(InternshipHead,on_delete=models.DO_NOTHING)
    guideTeacher = models.ForeignKey(Teachers,on_delete=models.DO_NOTHING)
    internShip   = models.ForeignKey(InternShip,on_delete=models.DO_NOTHING)
