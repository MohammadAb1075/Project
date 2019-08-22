from django.db import models
from django.contrib.auth.models import User
from research.models import Faculties, College, Major
from internship.models import Student, DepartmentHead, Teachers

class ProjectForm(models.Model):
    student              = models.ForeignKey(Student, on_delete=models.DO_NOTHING ,related_name='PFstudent')
    guideTeacher1        = models.ForeignKey('project.WaitingQueue', on_delete=models.DO_NOTHING ,related_name='PFguideteacher1')
    guideTeacher2        = models.ForeignKey('project.WaitingQueue', on_delete=models.DO_NOTHING ,related_name='PFguideteacher2')
    term                 = models.CharField(max_length=3)
    numberOfGuideTeacher = models.BooleanField()

class Request(models.Model):
    Student     = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    projectForm = models.ForeignKey(ProjectForm, on_delete=models.DO_NOTHING)
    text        = models.TextField()
    title       = models.TextField()

class ChooseGuideTeacherByStudent(models.Model):
    student       = models.ForeignKey(Student, on_delete=models.DO_NOTHING ,related_name='CGTBstudent')
    project       = models.ForeignKey(ProjectForm, on_delete=models.DO_NOTHING ,related_name='CGTBproject')
    guideTeacher1 = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING ,related_name='CGTBguideteacher1')
    guideTeacher2 = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING ,related_name='CGTBguideteacher2')


class ChooseAdvisorTeacher(models.Model):
    student        = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    advisorTeacher = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    projectForm    = models.ForeignKey(ProjectForm, on_delete=models.DO_NOTHING)


class WaitingQueue(models.Model):
    guideTeacher             = models.ForeignKey(ChooseGuideTeacherByStudent, on_delete=models.DO_NOTHING)
    project                  = models.ForeignKey('project.Project', on_delete=models.DO_NOTHING)
    guideTeacherConfirmation = models.BooleanField()

class ProjectKeywords(models.Model):
    keyword = models.CharField(max_length=31)

class ProposalForm(models.Model):
    projectForm              = models.ForeignKey(ProjectForm, on_delete=models.DO_NOTHING)
    projectKeywords          = models.ForeignKey(ProjectKeywords, on_delete=models.DO_NOTHING)
    advisorTeacher           = models.ForeignKey(ChooseAdvisorTeacher, on_delete=models.DO_NOTHING ,related_name='PFadvisorteacher')
    guideTeacher             = models.ForeignKey('project.ChooseGuideTeacherByDH', on_delete=models.DO_NOTHING ,related_name='PFguideteacher')
    englishTitle             = models.TextField()
    persionTitle             = models.TextField()
    description              = models.TextField()
    projectOutputDescription = models.TextField()
    guideTeacherConfirmation = models.BooleanField()

class ChooseGuideTeacherByDH(models.Model):
    projectform           = models.ForeignKey(ProjectForm, on_delete=models.DO_NOTHING)
    departmenthead        = models.ForeignKey(DepartmentHead, on_delete=models.DO_NOTHING)
    confirmedguideteacher = models.CharField(max_length=31)
    confirmationdate      = models.DateTimeField()

class ConfirmationProposal(models.Model):
    student             = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    projectForm         = models.ForeignKey(ProjectForm, on_delete=models.DO_NOTHING)
    departmentHead      = models.ForeignKey(DepartmentHead, on_delete=models.DO_NOTHING)
    approvalData        = models.DateTimeField()
    approvalStatus      = models.IntegerField()
    approvalAttachments = models.TextField()



Degrees = (
    ('degree1','a'),
    ('degree1','b'),
    ('degree1','c'),
    ('degree1','e'),
    ('degree1','f'),
    ('degree1','g'),
)


class Project(models.Model):
    student            = models.ForeignKey(ConfirmationProposal, on_delete=models.DO_NOTHING ,related_name='Prostudent')
    guideTeacher       = models.ForeignKey(ProposalForm, on_delete=models.DO_NOTHING ,related_name='ProguideTeacher')
    advisorTeacher     = models.ForeignKey(ProposalForm, on_delete=models.DO_NOTHING ,related_name='ProadvisorTeacher')
    judge              = models.ForeignKey('project.ChooseJudge', on_delete=models.DO_NOTHING ,related_name='Projudge')
    guideTeacherAccept = models.BooleanField()
    judgmentDate       = models.DateTimeField()
    grade              = models.FloatField()
    gradeText          = models.TextField()
    degree             = models.CharField(choices=Degrees, max_length=2)
    acceptanceStatus   = models.BooleanField()
    attachmenturl      = models.TextField()
    projectStatus      = models.IntegerField()

class ProjectUploadURL(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    url     = models.TextField()

class WeeklyReport(models.Model):
    Project                   = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    reportDate                = models.DateTimeField()
    weekNumber                = models.IntegerField()
    reportTitle               = models.CharField(max_length=63)
    reportAttachmentUploadUrl = models.TextField()
    reportText                = models.TextField()


class ChooseJudge(models.Model):
    judgeTeacher   = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    departmenthead = models.ForeignKey(DepartmentHead, on_delete=models.DO_NOTHING)
    project        = models.ForeignKey(Project, on_delete=models.DO_NOTHING)


class FirstJudgment(models.Model):
    judgeTeacher      = models.ForeignKey(Teachers, on_delete=models.DO_NOTHING)
    project           = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    meetingNeeded     = models.BooleanField()
    reportCorrection  = models.BooleanField()
    acceptance        = models.BooleanField()
    confirmationDate  = models.DateTimeField()
    judgeConfirmation = models.BooleanField()

class Criterion(models.Model):
    type = models.CharField(max_length=63)

class Description(models.Model):
    firstJudgment = models.ForeignKey(FirstJudgment, on_delete=models.DO_NOTHING)
    type          = models.ForeignKey(Criterion, on_delete=models.DO_NOTHING)
    text          = models.TextField()

class Scores(models.Model):
    firstJudgment = models.ForeignKey(FirstJudgment, on_delete=models.DO_NOTHING)
    type          = models.ForeignKey(Criterion, on_delete=models.DO_NOTHING)
    grade         = models.FloatField()

class ConfirmScores(models.Model):
    departmentHead     = models.ForeignKey(DepartmentHead, on_delete=models.DO_NOTHING)
    project            = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    dhConfirmationDate = models.DateTimeField()
    dhConfirmation     = models.BooleanField()

class Opinions(models.Model):
    person      = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    student     = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    seenDate    = models.DateTimeField()
    opinion     = models.TextField()
    opinionDate = models.DateTimeField()
    opinionText = models.TextField()

class ConfirmationWaitingQueue(models.Model):
    guideTeacher        = models.ForeignKey(WaitingQueue, on_delete=models.DO_NOTHING)
    guideTeacherOpinion = models.ForeignKey(Opinions, on_delete=models.DO_NOTHING)