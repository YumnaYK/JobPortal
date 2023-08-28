from dataclasses import dataclass, field
from datetime import date 
from utils.helpers import create_response 
from utils.responses import SUCCESSFUL, UNSUCCESSFUL, NOT_ELIGIBLE, DAYS_ERROR
from dateutil.parser import parse
from lms.serializers import LeaveRequestSerializer
from .models import LeaveTracker

@dataclass
class leave_intiate2:

    leave_id : int
    leave_lst : list
    start_date_str : date
    end_date_str : date

    serializer_class = LeaveRequestSerializer

    def calculate(self, request, employee_details, leave, minimum_service_period):
        
        start_date = parse(self.start_date_str).date()
        end_date = parse(self.end_date_str).date()
        days_of_service = (date.today() - employee_details.joining_date).days
        print("days_of_service", days_of_service)

        '''leave_name_mapping = {
            "annual":365,
            "casual":90
        }
        minimum_service_period = leave_name_mapping.get(leave.name.lower())'''
        if(leave.name.lower()== "annual"):
            minimum_service_period = 365
        elif (leave.name.lower() == "casual"):
            minimum_service_period = 90
            
        if (days_of_service >= minimum_service_period):
            print("minimum_service_period", minimum_service_period)
            total_days = (end_date - start_date).days + 1
            print("total_days", total_days)

            try:
                print("try enter")
                leave_balance = LeaveTracker.objects.get(user=employee_details.user, leave_type=leave.id)
                    #leave_balance.Available_Days = 5 - leave_balance.Available_Days
                    #leave_balance.save()
                print("leave_balance.Available_Days for (payload) leave intiated", leave_balance.Available_Days)
            except LeaveTracker.DoesNotExist:
                print("except enter")

                leave_balance = LeaveTracker.objects.create(user=employee_details.user, leave_type=leave.id, Available_Days=leave.allowed_days)
                print("LeaveTracker created for the user and leave type.")

            if total_days <= leave_balance.Available_Days:
                    
                print("leave_balance.Available_Days", leave_balance.Available_Days)
                leave_balance.Available_Days = leave_balance.Available_Days - total_days
                print("leave_balance.Available_Days after leaves approved!", leave_balance.Available_Days)
                leave_balance.save()

                serializer = self.serializer_class(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    data = serializer.data
                    msg = SUCCESSFUL
                    status_code = 201
                    return data, msg, status_code

                else:
                    data = serializer.errors
                    msg = UNSUCCESSFUL
                    status_code = 400
                    return data, msg, status_code
            else:
                data = {}
                msg = DAYS_ERROR
                status_code = 404
                return data, msg, status_code
        else:
            data = {}
            msg = NOT_ELIGIBLE
            status_code = 404
            return data, msg, status_code