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
    phone = serializers.CharField()
    address = serializers.CharField()
    internShipWebSite = serializers.CharField()
    term = serializers.CharField()

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
            internShipWebSite = data['internShipWebSite'],
            term = data['term']
        )
        form.save()
        return form
