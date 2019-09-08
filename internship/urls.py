from django.urls import path, re_path
from internship.views import *

urlpatterns = [
    # path('list/', views.user_list),
    # re_path('list/(?P<id>\d{0,10})', views.conversation_view),
    path('request/',RequestInternShipView.as_view()),
    path('checkfaculty/',CheckFacultyTrainingStaffView.as_view()),
    # path('checkdh/',CheckDepartmentHeadView.as_view()),
]
