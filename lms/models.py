from django.db import models
from utils.base_model import LogsMixin
from user_auth.models import User
from utils.validators import validate_file_size
# Create your models here.

class EmployeeDetails(LogsMixin):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="details")
    department = models.CharField(max_length=25,null=True, blank=True)
    designation = models.CharField(max_length=25,null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    reports_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #leave_balance = models.IntegerField(default=0)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="requested_leaves")
    leave_type = models.ManyToManyField(LeaveType, related_name="leave_name")
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateField()
    end_date = models.DateField()
    proof = models.FileField(validators=[validate_file_size], null=True, blank=True)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="manages")
    reason = models.CharField(max_length=150, null=True, blank=True)

class Notification(LogsMixin):
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)

class LeaveTracker(LogsMixin):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leaves_count")
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE, related_name="Lname")
    #leave_count = models.PositiveIntegerField()
    Available_Days = models.PositiveIntegerField(default=0) #remaining days of specific leave type for which user applied
