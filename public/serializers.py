from internship.models import Student
from rest_framework import serializers


class StudentSerilizer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = '__all__'


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

class ForgetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)
