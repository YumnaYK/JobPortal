from django.shortcuts import render
from rest_framework import viewsets
from .serializers import *
from .registration_controller import *
from utils.base_authentication import JWTAuthentication
# Create your views here.

reg_emp = RegistrationController()
emp_details = EmployeeDetailsController()
leave_type = LeaveTypeController()
leave_intiate = LeaveIntitateController()

class EmpRegAPI(viewsets.ModelViewSet):
    
    authentication_classes = (JWTAuthentication,)
    serializer_class = EmployeeRegistrationSerializer

    def post(self, request):
        return reg_emp.create_emp(request)
    
class EmpDetailsAPI(viewsets.ModelViewSet):

    serializer_class = EmployeeDetailsSerializer

    def post(self, request):
        return emp_details.add_employee_details(request)
    def get(self, request):
        return emp_details.get_employee_details(request)
    def update(self, request):
        return emp_details.update_employee_details(request)

class LeaveTypeAPI(viewsets.ModelViewSet):

    serializer_class = LeaveTypeSerializer

    def get(self, request):
        return leave_type.get_leave_types(request)
    def post(self, request):
        return leave_type.create_leave_type(request)
    def update(self, request):
        return leave_type.update_leave_type(request)
    def destory(self, request):
        return leave_type.delete_LT(request)
    
class LeaveRequestAPI(viewsets.ModelViewSet):

    serializer_class =LeaveRequestSerializer

    def post(self, request):
        return leave_intiate.create_leave(request)
    def get(self, request):
        return leave_intiate.get_leaves(request)

class Delete_Leave(viewsets.ModelViewSet):

    serializer_class = LeaveTypeSerializer

    def delete_LT(self, request):
        
        id = get_query_param(request, "id", None)
        print(id)
        
        if not id:
            return create_response({}, ID_NOT_PROVIDED, 404)
        instance = self.serializer_class.Meta.model.objects.filter(id=id).first()
        if not instance:
            return create_response({}, NOT_FOUND, status_code=400)
        instance.delete()
        return create_response({}, SUCCESSFUL, 200)

    