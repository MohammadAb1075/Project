import string
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.core.mail import send_mail, BadHeaderError

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from internship.models import Student

from Arion.utils import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication

from public.serializers import *

class SignUpView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
            {
                'Message' : 'Account Create',
                'data'  : serializer.data
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


class RequestForgetEmail(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    def post(self,request):
        request_serializer = ForgetEmailSerializer(data=request.data) #request.POST['email']

        if request_serializer.is_valid():
            print("*********************",User.objects.get(username=request_serializer.data['username']))
            if User.objects.get(username=request_serializer.data['email']) in User.objects:
                mail = request_serializer.data['email']
                mail = mail.split()
                send_mail('New Password', 'This is Your New Password !!!','utfarabi@gmail.com', mail)
                return Response(
                    {
                        'message':'A New Email Sended successfuly!!!'
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                {
                    'message':'there is No  Any Account With This Email'
                },
                 status=status.HTTP_404_FORBIDDEN
                )

        else:
            return Response(
             serial.errors,
             status=status.HTTP_400_BAD_REQUEST
            )


    def id_generator(size=6, chars=string.ascii_uppercase + string.ascii_lowercase+ string.digits):
        return ''.join(random.choice(chars) for _ in range(size))



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





def takeEmailLink(request):
    pass
