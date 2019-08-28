from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers
from public.models import Users,Student
from public.models import Faculties, College, Major

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id','first_name','last_name','username','password','role']
        # fields = '__all__'
    def create(self, data):
        u = Users(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
            role = data['role']
        )
        u.set_password(data['password'])
        u.save()
        return u


# class UserSerializer(serializers.ModelSerializer):
#     class Mete:
#         fields=['id','first_name','last_name','username','role']

class SignUpStudentSerializer(serializers.Serializer):

    # user           = models.ForeignKey(Users, on_delete=models.CASCADE)
    college        = serializers.IntegerField(min_value=1)
    faculty        = serializers.IntegerField(min_value=1)
    major          = serializers.IntegerField(min_value=1)
    credits        = serializers.IntegerField()
    average        = serializers.FloatField()
    studentNumber  = serializers.CharField(max_length=9)
    phone          = serializers.CharField(max_length=11)
    nationalCode   = serializers.CharField(max_length=10)
    name           = serializers.CharField(required= False,max_length=31)

    def create(self, data):
        c = College.objects.get(
        id=data['college'])
        f = Faculties.objects.get(
        id=data['faculty'])
        m = Major.objects.get(
        id=data['major'])

        s = Student(
            user          = self.context['user'],#self.context['user'],
            college       = c,
            faculty       = f,
            major         = m,
            credits       = data['credits'],
            average       = data['average'],
            studentNumber = data['studentNumber'],
            nationalCode  = data['nationalCode'],
            phone         = data['phone'],
            name          = data['name']
        )
        s.save()
        return s


class RequestSigninSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=30)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=128)


class ForgetEmailSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)



class EditProfileSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)
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
