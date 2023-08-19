from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user_auth.models import User
from django.contrib.auth.hashers import make_password
from utils.helpers import *
from utils.responses import *
from datetime import date
from .models import EmployeeDetails
from django.conf import settings
from dateutil.parser import parse
from .classes import *

class RegistrationController:

    serializer_class = EmployeeRegistrationSerializer
        
    def create_emp(self, request):
        
        email = request.data.get('email')
        password = request.data.get('password')
        hashed_password = make_password(password)

        if not email or not password:
            return Response({'error': 'Please provide both employee email and password'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if a user with the same email already exists
            if User.objects.filter(email=email).exists():
                return Response({'error': 'A user with this email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            request.data['password'] = hashed_password
            serializer = EmployeeRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class EmployeeDetailsController:

    serializer_class = EmployeeDetailsSerializer

    def add_employee_details(self, request):
        
        id = request.data.get("id")

        try:
            if not id:
                return create_response({}, ID_NOT_PROVIDED, 404)
            else:
                instance = User.objects.filter(id=id).first()
                if not instance:
                    return create_response({}, NOT_FOUND, 400)
                request.data["user"] = instance.id
                serialized_data = self.serializer_class(data=request.data)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return create_response(serialized_data.data, SUCCESSFUL, 200)
                return create_response({}, get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL), status_code=500)
        except Exception as e:
            print(e)
            return create_response({}, UNSUCCESSFUL, 406)
        
    def get_employee_details(self, request):

        kwargs = {}
        id = request.data.get("id")
        type = request.data.get("type")
        print(type)
        if id:
            kwargs["id"] = id
        if type:
            kwargs["user__type"] = type

        emp = self.serializer_class.Meta.model.objects.filter(**kwargs)

        serialized_data = self.serializer_class(emp, many=True).data
        response_data = {
            "data": serialized_data
        }
        return create_response(response_data, SUCCESSFUL, status_code=200)

    def update_employee_details(self, request):
        
        user_id = request.data.get("user_id")

        try:
            if not user_id:
                return create_response({}, ID_NOT_PROVIDED, 404)
            else:
                user_id = request.data.get("user_id")
                instance = self.serializer_class.Meta.model.objects.filter(user_id=user_id).first()
                if not instance:
                    return create_response({}, NOT_FOUND, 400)

                serialized_data = self.serializer_class(instance, data=request.data, partial=True)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return create_response(serialized_data.data, SUCCESSFUL, 200)
                return create_response({}, get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL), status_code=500)
        except Exception as e:
            print(e)
            return create_response({}, UNSUCCESSFUL, 406)

class LeaveTypeController():

    serializer_class = LeaveTypeSerializer

    def create_leave_type(self, request):  
        
        serializer = self.serializer_class(data=request.data)  
        if serializer.is_valid():  
            serializer.save()  
            return create_response(serializer.data, SUCCESSFUL, status_code=201)
        else:  
            return create_response(serializer.errors, UNSUCCESSFUL, status_code=404)
    
    def get_leave_types(self, request):

        kwargs = {}
        id = request.data.get("id")

        if id:
            kwargs["id"] = id

        leave = self.serializer_class.Meta.model.objects.filter(**kwargs)

        serialized_data = self.serializer_class(leave, many=True).data
        response_data = {
            "data": serialized_data
        }
        return create_response(response_data, SUCCESSFUL, status_code=200)
    
    def update_leave_type(self, request):
        
        id = request.data.get("id")

        try:
            if not id:
                return create_response({}, ID_NOT_PROVIDED, 404)
            else:
                instance = self.serializer_class.Meta.model.objects.filter(id=id).first()
                if not instance:
                    return create_response({}, NOT_FOUND, 400)

                serialized_data = self.serializer_class(instance, data=request.data, partial=True)
                if serialized_data.is_valid():
                    serialized_data.save()
                    return create_response(serialized_data.data, SUCCESSFUL, 200)
                return create_response({}, get_first_error_message_from_serializer_errors(serialized_data.errors, UNSUCCESSFUL), status_code=500)
        except Exception as e:
            print(e)
            return create_response({}, UNSUCCESSFUL, 406)

class LeaveIntitateController:

    serializer_class = LeaveRequestSerializer

    '''def send_response(self, request):

        id = request.data.get("user")
        instance = User.objects.filter(id=id).first()

        user_mail = instance.email
        first_name = instance.first_name
        last_name = instance.last_name
        
        
        try:
            if not user_mail:
                # if email not found return an error message
                return Response({'message': 'Email Not Found'})
                
            # Prepare the email subject and message
            subject = "Dummy Response"
            message = f"""
                Hi {first_name} {last_name},
                Your request for leave has been received.
                you'll get a response in a while !
                """
            recipient_list = [user_mail]
            
            # Send the email
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
            
            # Return success message
            return Response({'message': 'Email Successfully Sent'})

        except Exception as e:
            # Print the error message
            print(e)
            # Return error message
            return Response({'error': str(e)}, status=400)
     
    def send_leave_notification(self, instance, report_to):
        message = f"A new leave request has been initiated by {instance.username}. Please review and take necessary action."
        notification_data = {
            'recipient': report_to,
            'message': message
        }
        serializer = NotificationSerializer(data=notification_data)
        if serializer.is_valid():
            serializer.save()
            return create_response(serializer.data, SUCCESSFUL, 200)
        else:
            return create_response(serializer.errors, UNSUCCESSFUL, status_code=404)
        
    '''

class LeaveIntitateController2:
        
        def create_leave(self, request):  

            leave_id = request.data.get("leave_type")[0]
            leave = LeaveType.objects.get(id=leave_id)
            leave_name = leave.name
            start_date_str = request.data.get("start_date")
            end_date_str = request.data.get("end_date")
            id = request.data.get("user")
            instance = User.objects.filter(id=id).first()
            employee_details = EmployeeDetails.objects.filter(user=instance).first()


            application = leave_intiate2(leave_id, leave_name, start_date_str, end_date_str)
            application.calculate(request, employee_details, leave, 0)

            return create_response({}, SUCCESSFUL, status_code=201)
    