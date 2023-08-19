from django.shortcuts import render
from utils.base_authentication import JWTAuthentication
# Create your views here.
from rest_framework import viewsets
from user_auth.user_controller import *

login_controller = LoginController()
forget_password_controller = ForgetPasswordController()
change_password_controller = ChangePasswordController()
verify_otp = VerifyOtpController()
employee = EmployeeController()


class LoginAPIView(viewsets.ModelViewSet):
    """
        An endpoint for user login.
        """
    serializer_class = LoginSerializer

    def post(self, request):
        return login_controller.post(request)


class ChangePasswordAPI(viewsets.ModelViewSet):
    """
    An endpoint for changing password.
    """
    authentication_classes = (JWTAuthentication,)
    serializer_class = ChangePasswordSerializer

    def patch(self, request):
        return change_password_controller.update(request)


class ForgetPasswordAPI(viewsets.ModelViewSet):
    """
    An endpoint for forget password.
    """
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        return forget_password_controller.forget_password(request)


class VerifyOtpAPI(viewsets.ModelViewSet):
    """
    An endpoint for token verification.
    """
    serializer_class = VerifyOtpSerializer

    def post(self, request):
        return verify_otp.verify(request)
    
class EmployeeAPI(viewsets.ModelViewSet):
    """
    An endpoint for token verification.
    """
    authentication_classes = (JWTAuthentication,)
    serializer_class = GetEmployeeSerializer

    def get(self, request):
        return employee.get_employees(request)
    def destroy(self, request):
        return employee.delete_user(request)
    
