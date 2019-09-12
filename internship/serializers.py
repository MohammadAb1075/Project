import re
from datetime import datetime
from django.db.models import Q
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
        fields = ['first_name','last_name','username','date_joined','roles','last_login']


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
    user = UsreInformation()
    major = MajorInformation()
    class Meta:
        model = Student
        fields = '__all__'








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

class RequestInformationGETSerializer(serializers.ModelSerializer):
    internshipPlace = InternShipPlaceInformation()
    student = StudentInformationSerializer()
    class Meta:
        model = Request
        fields = '__all__'







class RequestFormInternShipSerializer(serializers.Serializer):
    nameplace = serializers.CharField()
    city = serializers.IntegerField(min_value=1)
    address = serializers.CharField()
    phone = serializers.CharField(max_length=15)
    internShipWebSite = serializers.CharField(required=False)
    term = serializers.CharField()
    title = serializers.CharField(required=False,allow_blank=True)
    state = serializers.IntegerField(required=False)

    def validate(self, data):
        x1 = re.findall("[a-z]", data['phone'])
        if x1 != []:
            print("***********",self.context['student'].credits)
            raise serializers.ValidationError(
                'The Phone Number Should Only Be In Number !!!'
            )
        if self.context['student'].credits < 80 :
            raise serializers.ValidationError(
                'Credits Error'
            )
        return data


    def create(self, data):

        ct=City.objects.get(id=data['city'])

        isp=InternShipPlace(
            city = ct,
            nameplace = data['nameplace'],
            address = data ['address']  ,
            phone = data['phone']
        )
        if 'internShipWebSite' in data:
            form.internShipWebSite = data['internShipWebSite']
        isp.save()


        request=Request.objects.create(
            student = self.context['student'],
            internshipPlace = isp,
            title = 'InternShip',
            term = data['term'],
            state = 1
        )
        request.save()

        if 'comment' in data:
            request.comment = data['comment']
        # request.save()
        # request.title='InternShip'
        print("***********",request.student.major)
        r=Role.objects.get(Q(role='FacultyTrainingStaff'))
        # print("***********",r.department.all()[0])
        u=Users.objects.get(roles=r)
        try:
            opinion=Opinion(
                user = u,
                request = request,
            )

            opinion.save()
            return request
        except:
            request.delete()
            isp.delete()
            raise serializers.ValidationError(
                'Error!!!'
            )

class OpinionSerializers(serializers.ModelSerializer):
    # user = UsreInformation()
    request = RequestInformationGETSerializer()
    class Meta:
        model = Opinion
        exclude=['user']


class RequestGetSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    last_name = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    username = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    title = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    
# class OpinionSerializers(serializers.Serializer):
#     request = RequestInformationGETSerializer()
#     seenDate = serializers.DateTimeField(required=False)
#     opinionDate = serializers.DateTimeField(required=False)
#     opinionText = serializers.CharField(required=False)
#
#     def update(self,instance ,validated_data):
#         instance.seenDate = datatime.now()
#         instance.save()
#         return  instance

















# class CheckInternShipSerializer(serializers.ModelSerializer):
#     student = StudentInformationSerializer()
#     class Meta:
#         model = InternshipForm
#         fields = '__all__'
