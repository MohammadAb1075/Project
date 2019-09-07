from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AnonymousUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from Arion.utils import CsrfExemptSessionAuthentication
from public.models import Users,Student
from internship.serializers import *



# class InternShipStateView(APIView):
#     def get(self, request):
#         internshipstate = InternShipState


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

            # ###Show Student Information
            # student = Student.objects.get(user = request.user)
            # isp = InternshipForm.objects.get(student=student)
            # serializer = ShowInternShipFormSerializer(instance=isp)
            #
            # return Response(
            #     {
            #         'data' : serializer.data
            #     },
            #     status=status.HTTP_200_OK
            # )


            ###Show Student Information
            student = Student.objects.get(user = request.user)
            serializer = StudentInformationSerializer(instance=student)

            if student.credits < 80 :
                return Response(
                        {
                            'message' : 'Credits Error',

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
            # serializer = InternShipFormSerializer(data=request.data)
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
                        'Message' : 'Form completed',
                    },
                    status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
    # def get(self,request):
    #     student = Student.objects.get(user = request.user)
    #     print("***************",student)
    #     isp = InternshipForm.objects.get(student=student)
    #     print("***************",isp)
    #





class CheckFacultyTrainingStaffView(APIView):
#     def get(self, request):
#         if type(request.user) is AnonymousUser :
#             return Response(
#                 {
#                     'message' : 'UnAuthorize !!!'
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
# # <Role: FacultyTrainingStaff>
#         # elif  request.user.roles.all() :
#         #     return Response(
#         #         {
#         #             'message' : 'InAccessibility !!!'
#         #         },
#         #         status=status.HTTP_403_FORBIDDEN
#         #     )
#         # print("***************",request.user.roles.all())
#         else:
#             request = Request.objects.all()
#             serializer = RequestInformationSerializer(instance=request, many=True)
#             # internshipform = InternshipForm.objects.all()
#             # serializer = ShowInternShipSerializer(instance=internshipform,many=True)
#             return Response(
#                 {
#                     'data' : serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )


    def get(self,request):
        # try:
        # request = Request.objects.all()
        request_serializer = RequestInformationGETSerializer(data=request.GET) #data=request.data
        print("***************************",request_serializer)
        if request_serializer.is_valid():
            request = Request.objects
            if 'first_name' in request_serializer.data:
                request = request.filter(
                internShipForm__student__users__first_name=request_serializer.data['first_name']
                )
            if 'last_name' in request_serializer.data:
                request = request.filter(
                    internShipForm__student__users__last_name=request_serializer.data['last_name']
                )
            if 'username' in request_serializer.data:
                request = request.filter(
                    internShipForm__student__users__username=request_serializer.data['last_name']
                )
            serializer=RequestInformationSerializer(instance=request,many=True)

            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                request_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        # except:
        #     request = Request.objects.all()
        #     # print("****************",request.objects.filter(internShipForm.student.users.first_name=request_serializer.data['first_name']))
        #     serializer = RequestInformationSerializer(request, many = True)
        #     return Response(
        #         {
        #             # 'data' : serializer.data
        #         },
        #         status=status.HTTP_200_OK
        #     )











    def post(self, request):
        if type(request.user) is AnonymousUser :
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            request = Request.objects.all()
            serializers = RequestInformationSerializer(instance=request, data=request.data, many=True)





# class CheckDepartmentHeadView(APIView):
#     def get(self, request):
#         if type(request.user) is AnonymousUser :
#             return Response(
#                 {
#                     'message' : 'UnAuthorize !!!'
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         elif request.user.role != 'DepartmentHead':
#             return Response(
#                 {
#                     'message' : 'InAccessibility !!!'
#                 },
#                 status=status.HTTP_403_FORBIDDEN
#             )
#         else:
#             print("******************",InternshipForm.objects.all()[0].student.major)
#             internshipform = InternshipForm.objects.all()
#             serializer = CheckInternShipSerializer(instance=internshipform,many=True)
#             return Response(
#                 {
#                     'data' : serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )
