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


class RequestInternShipView(APIView):
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
            # student = Student.objects.get(user = request.user)
            student = Student.objects.filter(user = request.user)[0]
            serializer = RequestFormInternShipSerializer(
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

    def put(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            editcredit = Student.objects.get(user = request.user)
            serializer = EditCreditsSerializer(instance=editcredit,data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    {
                        'message': 'Credits Edited successfuly',
                        'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class RequestFlowView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def get(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        student = Student.objects.get(user = request.user)
        opinion = Opinion.objects.get(request__student=student)

        serializer = RequestFlowSerializer(instance=opinion)

        return Response(
            {
                'data' : serializer.data
            },
            status=status.HTTP_200_OK
        )




class CheckRequestView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def get(self,request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        # for r in request.user.roles.all():
        #     r=str(r)
        #     print("***********************************",request.user)
        #     if r != 'FacultyTrainingStaff':
        #         return Response(
        #             {
        #                 'message' : 'InAccessibility !!!'
        #             },
        #             status=status.HTTP_403_FORBIDDEN
        #         )


        opinion_serializer = OpinionGetFilterSerializer(data=request.GET) #data=request.data
        if opinion_serializer.is_valid():
            print("***********************************",request.user.roles.all())
            for r in request.user.roles.all():
                r=str(r)
                if r == 'FacultyTrainingStaff':
                    opinion = Opinion.objects.filter(request__state=1)

                elif r == 'DepartmentHead':
                    opinion = Opinion.objects.filter(request__state=2)

                elif r == 'UniversityTrainingStaff':
                    opinion = Opinion.objects.filter(request__state=3)

                else:
                    return Response(
                        {
                            'message' : 'InAccessibility !!!'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )



            if 'first_name' in opinion_serializer.data:
                opinion = opinion.filter(
                    request__student__user__first_name=opinion_serializer.data['first_name']
                )
            if 'last_name' in opinion_serializer.data:
                opinion = opinion.filter(
                    request__student__user__last_name=opinion_serializer.data['last_name']
                )
            if 'username' in opinion_serializer.data:
                opinion = opinion.filter(
                    request__student__user__username=opinion_serializer.data['username']
                )
            if 'title' in opinion_serializer.data:
                opinion = opinion.filter(
                    request__title=opinion_serializer.data['title']
                )
            serializer=OpinionSerializers(instance=opinion,many=True)
            for op in opinion:
                print("*********************",op.seenDate)
                if op.seenDate is None:
                    op.seenDate=datetime.now()
                    op.save()

                # op.seenDate=datetime.now()
                # op.save()


            return Response(
                {
                    'data' : serializer.data
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                opinion_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request):
        if type(request.user) is AnonymousUser:
            return Response(
                {
                    'message' : 'UnAuthorize !!!'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            opinion = Opinion.objects.get(id = request.data['id'])
            serializer = OpinionEditSerializers(instance=opinion,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                    'message': 'Your Opinion Was Recorded Successfuly',
                    # 'data': serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(
                {
                "user" : serializer.data
                },
                status=status.HTTP_200_OK
            )


































# class CheckFacultyTrainingStaffView(APIView):
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#
#     def get(self,request):
#         if type(request.user) is AnonymousUser:
#             return Response(
#                 {
#                     'message' : 'UnAuthorize !!!'
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         for r in request.user.roles.all():
#             r=str(r)
#             print("***********************************",request.user)
#             if r != 'FacultyTrainingStaff':
#                 return Response(
#                     {
#                         'message' : 'InAccessibility !!!'
#                     },
#                     status=status.HTTP_403_FORBIDDEN
#                 )
#
#
#         opinion_serializer = OpinionGetFilterSerializer(data=request.GET) #data=request.data
#         if opinion_serializer.is_valid():
#             opinion = Opinion.objects.filter(request__state=1)
#             if 'first_name' in opinion_serializer.data:
#                 opinion = opinion.filter(
#                     request__student__user__first_name=opinion_serializer.data['first_name']
#                 )
#             if 'last_name' in opinion_serializer.data:
#                 opinion = opinion.filter(
#                     request__student__user__last_name=opinion_serializer.data['last_name']
#                 )
#             if 'username' in opinion_serializer.data:
#                 opinion = opinion.filter(
#                     request__student__user__username=opinion_serializer.data['username']
#                 )
#             if 'title' in opinion_serializer.data:
#                 opinion = opinion.filter(
#                     request__title=opinion_serializer.data['title']
#                 )
#             serializer=OpinionSerializers(instance=opinion,many=True)
#             for op in opinion:
#                 print("**********",op.seenDate)
#                 if op.seenDate is None:
#                     op.seenDate=datetime.now()
#                     op.save()
#             return Response(
#                 {
#                     'data' : serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )
#         else:
#             return Response(
#                 opinion_serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def put(self, request):
#         if type(request.user) is AnonymousUser:
#             return Response(
#                 {
#                     'message' : 'UnAuthorize !!!'
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         else:
#             opinion = Opinion.objects.get(id = request.data['id'])
#             serializer = OpinionEditSerializers(instance=opinion,data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(
#                     {
#                     'message': 'Your Opinion Was Recorded Successfuly',
#                     # 'data': serializer.data
#                     },
#                     status=status.HTTP_200_OK
#                 )
#             else:
#                 return Response(
#                     serializer.errors,
#                     status=status.HTTP_404_NOT_FOUND
#                 )
#
#             return Response(
#                 {
#                 "user" : serializer.data
#                 },
#                 status=status.HTTP_200_OK
#             )
