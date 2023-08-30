from django.db import models
from utils.base_model import LogsMixin
from user_auth.models import User
from utils.validators import validate_file_size
# Create your models here.

class EmployeeDetails(LogsMixin):

    APPROVAL_LEVEL_CHOICES = (
        ("CDO", "CDO"),
        ("LEAD", "LEAD"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="details")
    department = models.CharField(max_length=25,null=True, blank=True)
    designation = models.CharField(max_length=25,null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    team_lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    approval_level = models.CharField(max_length=4, choices=APPROVAL_LEVEL_CHOICES, null=True, blank=True)
    is_team_lead = models.BooleanField(default=False)

class LeaveType(LogsMixin):

    LEAVE_CHOICES = (
        ("annual", "annual"),("casual", "casual"),
        ("sick", "sick"),("maternity", "maternity"),
        ("paternity", "paternity"),("miscarriage", "miscarriage"),
        ("special", "special"),("special_hajj", "special_hajj"),
        ("other", "other"),
    )
    name = models.CharField(max_length=12, choices=LEAVE_CHOICES)
    allowed_days = models.PositiveIntegerField()

class LeaveRequest(LogsMixin):

    STATUS_CHOICES= (
        ("approved", "approved"),("pending", "pending"),
        ("rejected", "rejected"),
    )
    APPROVE_CHOICE = (
        ("from_lead", "from_lead"),
        ("from_cdo", "from_cdo"),
        ("approved", "approved")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_leaves")
    leave_type = models.ManyToManyField(LeaveType, related_name="leave_name")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateField()
    end_date = models.DateField()
    proof = models.FileField(validators=[validate_file_size], null=True, blank=True)
    reason = models.CharField(max_length=150, null=True, blank=True)
    current_approval_level = models.CharField(max_length=10, choices=APPROVE_CHOICE, null=True, blank=True, default="from_lead")

class Notification(LogsMixin):
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

class LeaveTracker(LogsMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaves_count")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name="Lname")
    Available_Days = models.PositiveIntegerField(default=0) #remaining days of specific leave type for which user applied
