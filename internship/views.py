from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from Arion.utils import CsrfExemptSessionAuthentication
from public.models import Users,Student
from internship.serializers import *



class InternShipFormView(APIView):
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
            ###Show Student Information
            student = Student.objects.get(user = request.user)
            serializer = StudentInformationSerializer(instance=student)

            if student.credits < 80 :
                return Response(
                        {
                            'message' : 'You Cant Send Internship Request!!!',

                            'data' : serializer.data
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )

            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )

    def post(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            student = Student.objects.get(user = request.user)
            serializer = InternShipFormSerializer(
                data=request.data,
                context={
                    'student'  : student
                    }
            )
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'Message' : 'Form completed'
                    }
                    )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
class CheckFacultyTrainingStaffView(APIView):
    def get(self, request):
        if type(request.user) is AnonymousUser :
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif request.user.role != 'FacultyTrainingStaff':
            return Response(
                {
                    'message' : 'InAccessibility !!!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:
            print("******************",request.user.role)
            internshipform = InternshipForm.objects.all()
            serializer = CheckInternShipSerializer(instance=internshipform,many=True)
            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )


class CheckDepartmentHeadView(APIView):
    def get(self, request):
        if type(request.user) is AnonymousUser :
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        elif request.user.role != 'DepartmentHead':
            return Response(
                {
                    'message' : 'InAccessibility !!!'
                },
                status=status.HTTP_403_FORBIDDEN
            )
        else:

            internshipform = InternshipForm.objects.all()
            serializer = CheckInternShipSerializer(instance=internshipform,many=True)
            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )
