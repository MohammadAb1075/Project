from django.contrib import admin

from public.models import *

admin.site.register(Users)
admin.site.register(Student)
admin.site.register(Teachers)
admin.site.register(DepartmentHead)
admin.site.register(FacultyTrainingStaff)
admin.site.register(UniversityTrainingStaff)

admin.site.register(Faculties)
admin.site.register(Department)
admin.site.register(College)
admin.site.register(Major)
# admin.site.register(User)
