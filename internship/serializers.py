import re
from rest_framework import serializers
from public.models import *
from internship.models import *




class RoleInformation(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UsreInformation(serializers.ModelSerializer):
    roles = RoleInformation(many=True)
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','roles']


class CollogeInformation(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class FacultyInformation(serializers.ModelSerializer):
    college = CollogeInformation()
    class Meta:
        model = Faculties
        fields = '__all__'

class MajorInformation(serializers.ModelSerializer):
    faculty = FacultyInformation()
    class Meta:
        model = Major
        fields = '__all__'


class StudentInformationSerializer(serializers.ModelSerializer):
    user  = UsreInformation()
    major = MajorInformation()
    class Meta:
        model = Student
        fields = '__all__'


class InternShipFormSerializer(serializers.Serializer):
    nameplace         = serializers.CharField(max_length=15)
    city              = serializers.IntegerField(min_value=1)
    address           = serializers.CharField()
    phone             = serializers.CharField()
    internShipWebSite = serializers.CharField(required=False)
    term              = serializers.CharField()

    # def validate(self, data):
    #     x1 = re.findall("[a-z]", data['phone'])
    #     if x1 != []:
    #         print("***********",self.context['student'].credits)
    #         raise serializers.ValidationError(
    #             'The Phone Number Should Only Be In Number !!!'
    #         )
    #     return data

    def create(self, data):
        ct = City.objects.get(id=data['city'])
        isp = InternShipPlace(
            nameplace = data['nameplace'],
            city = ct,
            address =  data['address'],
            phone = data['phone']
        )
        if 'internShipWebSite' in data:
            isp.internShipWebSite = data['internShipWebSite']
        isp.save()

        form=InternshipForm(
            internshipPlace = isp,
            student = self.context['student'],
            term = data['term']
        )
        form.save()

        r=Request(
            internShipForm =  form,
            title = 'InternShipRequest'
        )
        r.save()

        return form


class StateInformation(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

class CityInformation(serializers.ModelSerializer):
    state = StateInformation()
    class Meta:
        model = City
        fields = '__all__'

class InternShipPlaceInformation(serializers.ModelSerializer):
    city = CityInformation()
    class Meta:
        model = InternShipPlace
        fields = '__all__'



class InternShipInformation(serializers.ModelSerializer):
    student = StudentInformationSerializer()
    internshipPlace = InternShipPlaceInformation()
    class Meta:
        model = InternshipForm
        fields = '__all__'



class RequestInformationSerializer(serializers.ModelSerializer):
    internShipForm = InternShipInformation()
    class Meta:
        model = Request
        fields = '__all__'



class RequestInformationGETSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    usernaem = serializers.CharField(required=False)
