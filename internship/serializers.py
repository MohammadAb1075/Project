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


# class RequestInformationPOSTSerializer

class OpinionsSerializers(serializers.ModelSerializer):
    request = RequestInformationGETSerializer()
    class Meta:
        model = Opinions
        fields = '__all__'





class RequestInformationGETSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    usernaem = serializers.CharField(required=False)



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
            title='InternShip',
            term = data['term'],
            state = 1
        )

        if 'comment' in data:
            request.comment = data['comment']
        request.save()
        # request.title='InternShip'
        return request




class OpinionsSerializers(serializers.ModelSerializer):

    pass




















# class CheckInternShipSerializer(serializers.ModelSerializer):
#     student = StudentInformationSerializer()
#     class Meta:
#         model = InternshipForm
#         fields = '__all__'
