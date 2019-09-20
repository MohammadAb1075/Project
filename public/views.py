import string
import random
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import AnonymousUser
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from Arion.utils import CsrfExemptSessionAuthentication
from public.models import Users,Student
from public.serializers import *
from . import newpass
from .serializers import InboxSerializer
from internship.models import WeeklyReport,AttendanceTable
from request.models import Request
from internship.models import Opinion



class SignUpView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)

        # serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'Account Create',
                # 'data'  : serializer.data
            },
            status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUpStudentView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serializer = SignUpStudentSerializer(
            data = request.data,
            context = {
                'user' : request.user
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'Message' : 'The Account Creation Process completed',
                # 'data'  : serializer.data
            },
            status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )




class SignIn(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serial = RequestSigninSerializer(data=request.data)
        if serial.is_valid():
            user = authenticate(
                request,
                username=serial.data['username'],
                password=serial.data['password'])

            if user is None:
                    return Response(
                        {
                            'message': 'There is not any account with this username'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )

            login(request, user)
            return Response(
                {
                    'message': 'Your account info is correct',
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
             serial.errors,
             status=status.HTTP_400_BAD_REQUEST
            )


class EditProfile(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self, request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            information = Student.objects.get(user = request.user)
            serializer = StudentInformationSerializer(instance=information)
            # serializer = StudentInformationSerializer(instance=information,many=True)
            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )


    def put(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            information = Student.objects.get(user = request.user)
            serializer = EditProfileSerializer(instance=information,data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        'message': 'your account have been Edited successfuly',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RequestForgetEmail(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):

        serializer = ForgetEmailSerializer(data=request.data) #request.POST['email']
        if serializer.is_valid():
            try:
                user = Users.objects.get(username=serializer.data['username'])
            except ObjectDoesNotExist:
                return Response(
                    {
                        'message': 'There is not any account with this username'
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            newpassword = newpass.get_code(10)
            send_mail('New Password', 'This is Your New Password : {}'.format(newpassword),'utfarabi@gmail.com', user.username.split())
            user.set_password(newpassword)
            user.save()

            return Response(
                {
                    'message':'A New Email Sended successfuly!!!'
                },
                status=status.HTTP_200_OK
            )

        else:
            return Response(
             serializer.errors,
             status=status.HTTP_400_BAD_REQUEST
            )



class LogOutView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        else:
            request.session.flush()
            request.user = AnonymousUser()
            return Response(
                {
                    'message': 'Your account info is correct',
                },
                status=status.HTTP_200_OK
            )




class Inbox(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self, request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializedData = InboxSerializer(data=request.Get)
        if serializedData.is_valid():
            weeklyReport = WeeklyReport()
            attendanceTable = AttendanceTable()
            roll = InboxSerializer.data['userRole']
            user = Users.objects.get(user = request.user)
            if roll == 'FacultyTrainingStaff':
                request = Request.objects.filter(Q(applicant__major=user.roles.department) & Q(agreement__state__state=2))
                opinion = Opinion.objects.filter(request__state=1)
            elif roll == 'DepartmentHead':
                request = Request.objects.filter(Q(applicant__major=user.roles.department) & Q(agreement__state__state=1))
                opinion = Opinion.objects.filter(Q(user__roles__role='DepartmentHead') & Q(request__state=2))
            elif roll == 'UniversityTrainingStaff':
                request = Request.objects.filter(Q(applicant__major=user.roles.department) & Q(agreement__state__state=3))
                opinion = Opinion.objects.filter(Q(user__roles__role='UniversityTrainingStaff') & Q(request__state=3))
            elif roll == 'Teacher':
                request = Request.objects.filter(Q(applicant__major=user.roles.department) & Q(agreement__state__state=4))
                opinion = Opinion.objects.filter(Q(user__roles__role='UniversityTrainingStaff') & Q(request__state=3))
                weeklyReport = WeeklyReport.objects.filter(internShip__guideTeacher__user=request.user)
                attendanceTable = AttendanceTable.objects.filter(internShip__guideTeacher__user=request.user)






            else:
                return Response(
                    {
                        'message': 'InAccessibility !!!'
                    },
                    status=status.HTTP_403_FORBIDDEN
                )

            if 'first_name' in serializedData.data:
                opinion.filter(
                    request__student__user__first_name__contains = serializedData.data['first_name']
                )
                attendanceTable.objects.filter(
                    internShip__student__user__first_name__contain = serializedData.data['first_name']
                )
                request.filter(
                    applicant__user__first_name=serializedData.data['first_name']
                )
            if 'last_name' in serializedData.data:
                opinion.filter(
                    request__student__user__last_name__contains = serializedData.data['last_name']
                )
                attendanceTable.objects.filter(
                    internShip__student__user__last_name__contain=serializedData.data['last_name']
                )
                request.filter(
                    applicant__user__first_name__contain=serializedData.data['last_name']
                )

