from django.urls import path, include
from .views import *

urlpatterns = [
    path('employee_reg', EmpRegAPI.as_view({"post": "post"})),
    path('employee_details', EmpDetailsAPI.as_view(
        {
            "post": "post",
            "get": "get", 
            "patch": "update"
        }
    )
        ),
    path('leave_type', LeaveTypeAPI.as_view(
        {
            "get": "get",
            "post": "post",
            "patch": "update",
        }
    )
        ),
    path('leave_request', LeaveRequestAPI.as_view({"post": "post", "get": "get",})),
    path('delete', Delete_Leave.as_view({"delete": "delete_LT"})),
    path('leave_approve', LeaveApproveAPI.as_view(
            {
                "get": "get",
                "patch": "update"
            }
        )
            ),
]