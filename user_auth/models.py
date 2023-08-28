from django.db import models
from utils.base_model import LogsMixin
from django.contrib.auth.models import AbstractUser
from LeavePortal.settings import *
from utils.helpers import *

class User(LogsMixin, AbstractUser):

    USER_CHOICES = (
        ('admin', 'admin'),
        ('employee', 'employee'),
    )
    type = models.CharField(max_length=8, choices=USER_CHOICES, null=True, blank=True)
    emp_id = models.IntegerField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=25, null=True, blank=True)
    email = models.EmailField(unique=True)
    otp = models.IntegerField(null=True, blank=True)
    otp_generated_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    REQUIRED_FIELDS = ["username", "password"]
    USERNAME_FIELD = "email"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_access_token(self):
        return generate_access_token(self)
    
class Token(LogsMixin):
    """Token model for authentication"""

    user = models.ForeignKey(
        AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE, related_name="token"
    )
    token = models.TextField(max_length=500, unique=True, null=False, blank=False)

