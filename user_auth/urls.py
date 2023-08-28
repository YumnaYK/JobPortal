from django.urls import path, include
from user_auth.views import *

urlpatterns = [
    path('login', LoginAPIView.as_view({"post": "post"})),
    path('change-password', ChangePasswordAPI.as_view({"post": "patch"})),
    path('forget-password', ForgetPasswordAPI.as_view({"post": "post"})),
    path('verify-otp', VerifyOtpAPI.as_view({"post": "post"})),
    path('employees', EmployeeAPI.as_view({"get": "get", "delete": "destroy",})),
]