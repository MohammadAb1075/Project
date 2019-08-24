from django.urls import path, re_path, include
from django.views.decorators.csrf import csrf_exempt
from . import views
urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('signin/',csrf_exempt(views.SignIn.as_view())),
    path('editprofile/', views.EditProfile.as_view()),
    path('email/', views.RequestForgetEmail.as_view()),
    # path('forgetpassword/', views.RequestForgetEmail.as_view()),
    ]
