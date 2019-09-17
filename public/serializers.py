import re
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework import serializers
from public.models import Users,Student,Role
from public.models import College,Faculties,Department,Major





# class SignUpSerializer(serializers.ModelSerializer):
#     # roles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
#     class Meta:
#         model = Users
#         fields = ['id','first_name','last_name','username','password','roles']
#         # fields = '__all__'

    # def validate(self, data):
    #     # if data['role'] == 'Student':
    #     if 1 in data['role']:
    #         if len(data['role'])>1:
    #             raise serializers.ValidationError(
    #                 'Student Can not Have Any Other Role !!!'
    #             )
    #         x = re.search("@ut.ac.ir", data['username'])
    #         if x is None:
    #             raise serializers.ValidationError(
    #                 'Username Must Be Tehran University Email!!!'
    #             )
    #     return data


class SignUpSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=31)
    last_name = serializers.CharField(max_length=31)
    username = serializers.EmailField(max_length=31)
    password = serializers.CharField(max_length=31)
    role =  serializers.CharField(max_length=31)
    departmentName = serializers.CharField(max_length=63)

    def create(self, data):
        try:
            d=Department.objects.filter(departmentName=data['departmentName'])[0]
        except:
            fac= Faculties.objects.get(name = 'Engineering')
            d=Department(
                faculty = fac,
                departmentName = data['departmentName']
                )
            d.save()
        try:
            r=Role.objects.filter(Q(role=data['role']) & Q(department=d))[0]
        except:
            r=Role(
                role=data['role']
            )

            r.save()
            r.department.add(d)
            r.save()

        u = Users(
            first_name = data['first_name'],
            last_name = data['last_name'],
            username = data['username'],
        )
        u.set_password(data['password'])
        u.save()
        u.roles.add(r)
        u.save()
        return u







class SignUpStudentSerializer(serializers.Serializer):

    # college        = serializers.IntegerField(min_value=1)
    # faculty        = serializers.IntegerField(min_value=1)
    major          = serializers.IntegerField(min_value=1)
    credits        = serializers.IntegerField(min_value=0,max_value=150)
    average        = serializers.FloatField(min_value=1,max_value=20)
    studentNumber  = serializers.CharField(max_length=9)
    phone          = serializers.CharField(max_length=11)
    nationalCode   = serializers.CharField(max_length=10)
    name           = serializers.CharField(required=False,max_length=31)

    def create(self, data):
        # c = College.objects.get(
        # id=data['college'])
        # f = Faculties.objects.get(
        # id=data['faculty'])
        m = Major.objects.get(
        id=data['major'])

        s = Student(
            user          = self.context['user'],#self.context['user'],
            # college       = c,
            # faculty       = f,
            major         = m,
            credits       = data['credits'],
            average       = data['average'],
            studentNumber = data['studentNumber'],
            nationalCode  = data['nationalCode'],
            phone         = data['phone'],
            # name          = data['name']
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




class EditProfileSerializer(serializers.Serializer):
    password = serializers.CharField(required=False)
    credits  = serializers.IntegerField(required=False)
    average  = serializers.FloatField(required=False)
    phone    = serializers.CharField(required=False)


    def update(self, instance, validated_data):

        if  'password' in  validated_data:
            instance.user.set_password(validated_data['password'])
            instance.user.save()

        if 'credits' in  validated_data:
            instance.credits  = validated_data['credits']

        if  'average' in  validated_data:
            instance.average  = validated_data['average']

        if 'phone' in validated_data:
            instance.phone  = validated_data['phone']


        instance.save()
        return  instance



class InboxSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    startDate = serializers.CharField(required=False)
    endDate = serializers.CharField(required=False)
    isArchive =serializers.BooleanField(default=False)
    isStared = serializers.BooleanField(default=False)
    userRole = serializers.CharField(required=True)
