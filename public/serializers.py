from django.contrib.auth.models import User
from rest_framework import serializers
from internship.models import Student



class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','first_name','last_name','username','password']

    def create(self, data):
        u = User(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
        )
        u.set_password(data['password']

        )
        u.save()
        return u


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         exclude = ['password']


class RequestSigninSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True, allow_blank=False, max_length=30)
    password = serializers.CharField(
        required=True, allow_blank=False, max_length=128)

#
# class StudentSerilizer(serializers.ModelSerializer):
#     user = UserSerializer(many = True)
#     class Meta:
#         model  = Student
#         fields = '__all__'
#
#
#     def create(self, data):
#         u = User(
#             first_name = data['first_name'],
#             last_name  = data['last_name'],
#             username   = data['username'],
#             email      = data['email']
#         )
#         u.set_password(data['password'])
#         u.save()
#         return u


class ForgetEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, allow_blank=False)



class EditProfileSerializer(serializers.Serializer):
    credits = serializers.IntegerField(required=False)
    average = serializers.IntegerField(required=False)
    image   = serializers.ImageField(required=False)
    email   = serializers.EmailField(required=False)


    def update(self,instance ,validated_data):
        instance.credits = validated_data['credits']
        instance.average = validated_data['average']
        instance.image   = validated_data['image']
        instance.save()
        return  instance
