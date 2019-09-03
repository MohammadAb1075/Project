import re
from rest_framework import serializers
from public.models import *
from internship.models import *


class UsreInformation(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','date_joined','role','last_login']

class CollogeInformation(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class FacultyInformation(serializers.ModelSerializer):
    class Meta:
        model = Faculties
        fields = '__all__'
class MajorInformation(serializers.ModelSerializer):
    class Meta:
        model = Major
        fields = '__all__'

class StudentInformationSerializer(serializers.ModelSerializer):
    user = UsreInformation()
    college = CollogeInformation()
    faculty = FacultyInformation()
    major = MajorInformation()
    class Meta:
        model = Student
        fields = '__all__'


# class InternShipFormSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InternshipForm
#         fields = '__all__'

class InternShipFormSerializer(serializers.Serializer):
    state = serializers.IntegerField(min_value=1)
    city = serializers.IntegerField(min_value=1)
    internShipPlace = serializers.CharField()
    phone = serializers.CharField(max_length=15)
    address = serializers.CharField()
    internShipWebSite = serializers.CharField(required=False)
    term = serializers.CharField()
    nameIH = serializers.CharField()
    phoneIH =serializers.CharField(max_length=15)
    emailIH = serializers.EmailField()


    def validate(self, data):
        x1 = re.findall("[a-z]", data['phone'])
        x2 = re.findall("[a-z]", data['phoneIH'])
        if x1 != [] or x2 != []:
            print("***********",self.context['student'].credits)
            raise serializers.ValidationError(
                'The Phone Number Should Only Be In Number !!!'
            )
        return data


    def create(self, data):

        # isp=InternShipPlace(
        #     name = data['internShipPlace']
        # ).save()
        st=State.objects.get(id=data['state'])
        ct=City.objects.get(id=data['city'])

        form=InternshipForm(
            student = self.context['student'],
            state = st,
            city = ct,
            internShipPlace = data['internShipPlace'],
            phone = data['phone'],
            address = data ['address'],
            term = data['term'],
            nameIH = data['nameIH'],
            phoneIH = data['phoneIH'],
            emailIH = data['emailIH']
        )
        if 'internShipWebSite' in data:
            form.internShipWebSite = data['internShipWebSite']

        form.save()
        return form



class CheckInternShipSerializer(serializers.ModelSerializer):
    student = StudentInformationSerializer()
    class Meta:
        model = InternshipForm
        fields = '__all__'
