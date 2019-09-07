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


# class InternShipInformation(serializers.ModelSerializer):
#     class Meta:
#         model = InternshipForm
#         fields ='__all__'

class RequestInformationSerializer(serializers.ModelSerializer):
    # internShipForm = InternShipInformation()
    class Meta:
        model = Request
        fields = 'all'



class RequestInformationGETSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    usernaem = serializers.CharField(required=False)

# class InternShipFormSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = InternshipForm
#         fields = '__all__'

class InternShipFormSerializer(serializers.Serializer):
    nameplace = serializers.IntegerField(min_value=1)
    city = serializers.IntegerField(min_value=1)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=15)
    internShipWebSite = serializers.CharField(required=False)
    term = serializers.CharField()



    def validate(self, data):
        x1 = re.findall("[a-z]", data['phone'])
        if x1 != []:
            print("***********",self.context['student'].credits)
            raise serializers.ValidationError(
                'The Phone Number Should Only Be In Number !!!'
            )
        return data


    def create(self, data):

        ct=City.objects.get(id=data['city'])

        isp=InternShipPlace(
            city = ct,
            nameplace = data['internShipPlace'],
            address = data ['address']  ,
            phone = data['phone']
        )
        if 'internShipWebSite' in data:
            form.internShipWebSite = data['internShipWebSite']
        isp.save()


        request=Request(
            student = self.context['student'],
            internShipPlace = isp,
            term = data['term'],
            title='InternShip',
            if 'comment' in data:
                request.comment = data['internShipWebSite']
        )
        request.save()
        return request


#
# class CheckInternShipSerializer(serializers.ModelSerializer):
#     student = StudentInformationSerializer()
#     class Meta:
#         model = InternshipForm
#         fields = '__all__'
