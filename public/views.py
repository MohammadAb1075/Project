from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
# from public.functions import email
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from internship.models import Student
# from public.forms import PasswordResetRequestForm
from public.serializers import *

from rest_framework.authentication import SessionAuthentication, BasicAuthentication



# @api_view(['POST'])
class signIn(APIView):
    # authentication_classes = (CsrfExemtSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serial = StudentSerilizer(data=request.data)
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



class EditProfile(APIView):

    def put(self,request):

        serializer = EditProfileSerializer(data=request.data)

        if serializer.is_valid():

            serializer.update(request.user,request.data)

            return Response({
                'message': 'your account have been Edited successfuly',
                'data': serializer.data
            })
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )



class RequestForgetemail(APIView):

    def post(self,request):
        request_serializer = ForgetEmailSerializer(data=request.data) #request.POST['email']

        if request_serializer.is_valid():
            if User.objects.filter(email__exact=email):
                try:
                    # email('this is subject', 'this is text')
                    return Response(status=status.HTTP_200_OK)

                except:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


def takeEmailLink(request):
    pass