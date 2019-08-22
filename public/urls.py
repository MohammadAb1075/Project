from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('signin/',csrf_exempt(views.signIn.as_view())),
    path('editprofile/', views.EditProfile.as_view()),
    path('email/', views.RequestForgetemail.as_view()),
    ]

