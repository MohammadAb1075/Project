from django.contrib.auth.models import User
from rest_framework import serializers
from internship.models import Student

from django.utils.datastructures import MultiValueDictKeyError


class RoleSignUpSerializer(serializers.ModelSerializer):
    class Mete:
        model = User
        fields = ['id','first_name','last_name']






class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','password']
        # fields = '__all__'
    def create(self, data):
        u = User(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
        )
        u.set_password(data['password'])
        u.save()
        return u


class RequestSigninSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=30)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=128)


class ForgetEmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)



class EditProfileSerializer(serializers.Serializer):
    # password = serializers.CharField(required=False)
    credits  = serializers.IntegerField(required=False)
    average  = serializers.IntegerField(required=False)
    # image    = serializers.ImageField(required=False)
    phone    = serializers.CharField(required=False)


    def update(self,instance ,validated_data):

        instance.password = validated_data['password']
        instance.credits  = validated_data['credits']
        instance.average  = validated_data['average']
        # instance.image    = validated_data['image']
        instance.phone    = validated_data['phone']


        instance.save()
        return  instance
