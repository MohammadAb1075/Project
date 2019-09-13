import re
from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from public.models import *
from internship.models import *

class CollogeInformation(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'


class FacultyInformation(serializers.ModelSerializer):
    college = CollogeInformation()
    class Meta:
        model = Faculties
        fields = '__all__'

class DepartmentInformation(serializers.ModelSerializer):
    faculty = FacultyInformation()
    class Meta:
        model = Department
        fields = '__all__'

class RoleInformation(serializers.ModelSerializer):
    department = DepartmentInformation(many=True)
    class Meta:
        model = Role
        fields = '__all__'

class UsreInformation(serializers.ModelSerializer):
    roles = RoleInformation(many=True)
    class Meta:
        model = Users
        fields = ['first_name','last_name','username','date_joined','roles','last_login']

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
    reqdate = serializers.DateTimeField(required=False)


    def validate(self, data):
        x1 = re.findall("[a-z]", data['phone'])
        if x1 != []:

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
            reqdate = datetime.now(),
            state = 1
        )
        request.save()

        if 'comment' in data:
            request.comment = data['comment']
        r=Role.objects.get(Q(role='FacultyTrainingStaff'))
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




class EditCreditsSerializer(serializers.Serializer):
    credits  = serializers.IntegerField(required=False)

    def update(self, instance, validated_data):
        if 'credits' in  validated_data:
            instance.credits  = validated_data['credits']

        instance.save()
        return  instance




class OpinionSerializers(serializers.ModelSerializer):
    # user = UsreInformation()
    request = RequestInformationGETSerializer()
    class Meta:
        model = Opinion
        exclude=['user']



class OpinionGetFilterSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    last_name = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    username = serializers.CharField(
        required=False, allow_blank=False, max_length=100)
    title = serializers.CharField(
        required=False, allow_blank=False, max_length=100)



class OpinionEditSerializers(serializers.Serializer):
    seenDate = serializers.DateTimeField(required=False)
    opinionDate = serializers.DateTimeField(required=False)
    opinionText = serializers.CharField(required=False,allow_blank=True)
    opinion = serializers.BooleanField()

    def update(self,instance,validated_data):

        if  'opinion' in  validated_data:
            instance.opinionDate = datetime.now()
            if validated_data['opinion'] == 1:
                instance.request.opinion = validated_data['opinion']
                instance.request.state += 1
                instance.seenDate = None
                instance.request.save()

                if instance.request.state == 2:
                    r=Role.objects.get(Q(role='DepartmentHead'))
                    u=Users.objects.get(roles=r)
                    instance.user=u
                    instance.save()

                if instance.request.state == 3:
                    r=Role.objects.get(Q(role='UniversityTrainingStaff'))
                    u=Users.objects.get(roles=r)
                    instance.user=u
                    instance.save()

            else:
                for r in instance.user.roles.all():
                    r=str(r)
                    if r == 'FacultyTrainingStaff':
                        instance.request.state = 1
                    if r == 'DepartmentHead':
                        instance.request.state = 2
                    if r == 'UniversityTrainingStaff':
                        instance.request.state = 3
                    instance.request.opinion = 0
                    instance.request.save()


        if  'opinion' in  validated_data:
            instance.opinionText = validated_data['opinionText']

        instance.save()
        return instance



















class RoleInformationFlowSerializer(serializers.ModelSerializer):
    # department = DepartmentInformation(many=True)
    class Meta:
        model = Role
        fields = ['role']

class UsreInformationFlowSerializer(serializers.ModelSerializer):
    roles = RoleInformationFlowSerializer(many=True)
    class Meta:
        model = Users
        fields = ['roles']

class RequestInformationGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['title','state','reqdate']

class RequestFlowSerializer(serializers.ModelSerializer):
    user = UsreInformationFlowSerializer()
    request = RequestInformationGETSerializer()
    class Meta:
        model=Opinion
        fields='__all__'
