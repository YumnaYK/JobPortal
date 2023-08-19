from dataclasses import dataclass
from datetime import date 
from utils.helpers import create_response 
from utils.responses import SUCCESSFUL, UNSUCCESSFUL, NOT_ELIGIBLE, DAYS_ERROR
from dateutil.parser import parse
from .serializers import LeaveRequestSerializer, LeaveTrackerSerializer
from .models import LeaveTracker

@dataclass
class leave_intiate2:

    leave_id : int 
    leave_name : str
    start_date_str : date
    end_date_str : date

    serializer_class = LeaveRequestSerializer

    def calculate(self, request, employee_details, leave, minimum_service_period):
        
        start_date = parse(self.start_date_str).date()
        end_date = parse(self.end_date_str).date()
        days_of_service = (date.today() - employee_details.joining_date).days
    
        if self.leave_name == "annual":
            minimum_service_period = 365

        elif self.leave_name == "casual":
            minimum_service_period = 90
            
        if (days_of_service >= minimum_service_period):
            
            total_days = (end_date - start_date).days + 1

            try:
                leave_balance = LeaveTracker.objects.get(user=employee_details.user, leave_type=leave)
                #leave_balance.Available_Days = 5 - leave_balance.Available_Days
                #leave_balance.save()
                print("leave_balance.Available_Days for (payload) leave intiated", leave_balance.Available_Days)
            except LeaveTracker.DoesNotExist:
                
                leave_balance = LeaveTracker.objects.create(user=employee_details.user, leave_type=leave, Available_Days=leave.allowed_days)
                print("LeaveTracker created for the user and leave type.")

            if total_days <= leave_balance.Available_Days:
                    
                    print("leave_balance.Available_Days", leave_balance.Available_Days)
                    leave_balance.Available_Days = leave_balance.Available_Days - total_days
                    print("leave_balance.Available_Days after leaves approved!", leave_balance.Available_Days)
                    leave_balance.save()
                    breakpoint()
                    serializer = self.serializer_class(data=request.data)  
                    if serializer.is_valid():  
                        serializer.save()
                        return create_response(serializer.data, SUCCESSFUL, status_code=201)
                    else:
                        return create_response(serializer.errors, UNSUCCESSFUL, status_code=404)
            else:
                return create_response({}, DAYS_ERROR, status_code=404)
        else:
            return create_response({}, NOT_ELIGIBLE, status_code=404)
        
        

