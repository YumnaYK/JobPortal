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
import ast
from datetime import date
from utils.helpers import create_response
from utils.responses import SUCCESSFUL, UNSUCCESSFUL, NOT_ELIGIBLE, DAYS_ERROR
from dateutil.parser import parse

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
        print("id",id)
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

    def create_leave(self, request):

        start_date = parse(request.data.get("start_date")).date()
        end_date = parse(request.data.get("end_date")).date()

        print(start_date)
        print(end_date)

        id = request.data.get("user")
        instance = User.objects.filter(id=id).first()

        leave = request.data.get("leave_type")
        print("leave", leave)  # Check the value to ensure it's in the expected format

        leave_type_ids = [int(leave_id) for leave_id in leave.split(",")]
        print("leave_type_ids", leave_type_ids)

        leave_instance = LeaveType.objects.filter(id__in=leave_type_ids)
        print(leave_instance)

        request.POST._mutable = True
        pop_instances = request.data.pop("leave_type")
        print("pop_instances", pop_instances)

        if not instance or not leave_instance:
            return create_response({}, NOT_FOUND, 400)

        responses = []

        for leave in leave_instance:
            print(leave.id)
            print(leave.name)
            print(leave.allowed_days)

            employee_details = EmployeeDetails.objects.filter(user=instance).first()
            days_of_service = (date.today() - employee_details.joining_date).days
            print("days_of_service", days_of_service)

            leave_name_mapping = {
                "annual": 365,
                "casual": 90
            }
            minimum_service_period = leave_name_mapping.get(leave.name.lower(), 0)
            print("minimum_service_period",minimum_service_period)

            if (days_of_service >= minimum_service_period):
                print("minimum_service_period", minimum_service_period)
                total_days = (end_date - start_date).days + 1
                print("total_days", total_days)

                try:
                    print("try enter")
                    leave_type_instance = LeaveType.objects.get(id=leave.id)  # Fetch the LeaveType instance
                    leave_balance = LeaveTracker.objects.get(user=employee_details.user, leave_type=leave_type_instance)

                    print("leave_balance.Available_Days for (payload) leave initiated", leave_balance.Available_Days)

                except LeaveTracker.DoesNotExist:  # Use LeaveTracker.DoesNotExist here
                    print("except enter")

                    leave_balance = LeaveTracker.objects.create(user=employee_details.user,
                                                                leave_type=leave_type_instance,
                                                                Available_Days=leave.allowed_days)
                    print("LeaveTracker created for the user and leave type.")

                if total_days <= leave_balance.Available_Days:

                    print("leave_balance.Available_Days", leave_balance.Available_Days)
                    leave_balance.Available_Days = leave_balance.Available_Days - total_days
                    print("leave_balance.Available_Days after leaves approved!", leave_balance.Available_Days)
                    leave_balance.save()

                    serializer = self.serializer_class(data=request.data)
                    request.data['leave_type'] = leave.id

                    if serializer.is_valid():
                        serializer.save()
                        data = serializer.data
                        msg = SUCCESSFUL
                        status_code = 201

                    else:
                        data = serializer.errors
                        msg = UNSUCCESSFUL
                        status_code = 400
                else:
                    data = {}
                    msg = DAYS_ERROR
                    status_code = 400
            else:
                print("Else enter last ")
                data = {}
                msg = NOT_ELIGIBLE
                status_code = 400

            responses.append({
                "data": data,
                "msg": msg,
                "status_code": status_code
            })

        return create_response(responses, "Responses for leave requests", 200)

    def get_leaves(self, request):

        leave = self.serializer_class.Meta.model.objects.filter()

        serialized_data = self.serializer_class(leave, many=True).data
        response_data = {
            "data": serialized_data
        }
        return create_response(response_data, SUCCESSFUL, status_code=200)

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
            return Response({'message': 'Email Successfully Sent'})def send_response(self, request):

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
class LeaveApprovalController:
    def leave_approval_view(self, request):

        current_user = request.user
        current_employee = current_user.details

        print("current_employee", current_employee)

        if current_employee.approval_level == 'LEAD':
            print(current_employee.approval_level)
            pending_requests = LeaveRequest.objects.filter(status='pending', current_approval_level='from_lead')
            print(pending_requests)

        elif current_employee.approval_level == 'CDO':
            print("current_employee.approval_level", current_employee.approval_level)
            pending_requests = LeaveRequest.objects.filter(status='pending', current_approval_level='from_cdo')
            print(pending_requests)

        return create_response({}, SUCCESSFUL, status_code=200)

    def approve_leave(self, request):

        current_user = request.user
        leave_request = LeaveRequest.objects.get(id=request.data.get("request_id"))
        print(leave_request)

        if current_user != leave_request.user:

            if current_user.details.approval_level == "LEAD" and leave_request.current_approval_level == "from_lead":
                # Team Lead approval
                leave_request.current_approval_level = "from_cdo"
                leave_request.save()

                # Notify the CDO
                #message = f"Leave request from {leave_request.start_date} to {leave_request.end_date} requires your approval."
                #Notification.objects.create(recipient=leave_request.manager, message=message)
                return create_response({}, SUCCESSFUL, status_code=200)

            elif current_user.details.approval_level == "CDO" and leave_request.current_approval_level == "from_cdo":
                # COD approval
                leave_request.current_approval_level = "approved"
                leave_request.status = "approved"
                leave_request.save()
                return create_response({}, SUCCESSFUL, status_code=200)
        else:
            return create_response({}, SAME_USER, status_code=400)

        return create_response({}, SUCCESSFUL, status_code=200)
