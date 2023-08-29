from rest_framework import serializers
from .models import *

class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    """employee register serializer
    """
    email = serializers.EmailField(
        label="email",
        write_only=True
    )
    password = serializers.CharField(
        label="password",
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True
    )
    
    def validate(self, instance):
        if len(instance["password"]) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return instance
    
    class Meta:
        model = User
        fields = "__all__"
    
class EmployeeDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmployeeDetails
        fields = "__all__"

class LeaveTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LeaveType
        fields = "__all__"

class LeaveRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        fields = "__all__"

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ("recipient","message")
