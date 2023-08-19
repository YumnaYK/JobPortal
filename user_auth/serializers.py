from rest_framework import serializers
from .models import User
from lms.serializers import EmployeeDetailsSerializer

class LoginSerializer(serializers.Serializer):

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

class ChangePasswordSerializer(serializers.Serializer):
  
    old_password = serializers.CharField(
        label="old_password",
        style={"input_type": "old_password"},
        trim_whitespace=False,
        write_only=True
    )

    new_password = serializers.CharField(
        label="new_password",
        style={"input_type": "new_password"},
        trim_whitespace=False,
        write_only=True
    )

    confirm_password = serializers.CharField(
        label="confirm_password",
        style={"input_type": "confirm_password"},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, instance):
        user = self.context.get("user")
        if len(instance["new_password"]) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return instance


class VerifyOtpSerializer(serializers.Serializer):
   
    otp = serializers.CharField(
        label="otp",
        style={"input_type": "otp"},
        trim_whitespace=False,
        write_only=True
    )

    new_password = serializers.CharField(
        label="new_password",
        style={"input_type": "new_password"},
        trim_whitespace=False,
        write_only=True
    )

    confirm_password = serializers.CharField(
        label="confirm_password",
        style={"input_type": "confirm_password"},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, instance):
        user = self.context.get("user")
        if len(instance["new_password"]) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return instance


class ForgetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField(
        label="email",
        write_only=True
    )

class GetEmployeeSerializer(serializers.ModelSerializer):

    employee_details = serializers.SerializerMethodField()
    
    def get_employee_details(self, instance):
        
        try:
            data = EmployeeDetailsSerializer(instance.details).data
            
        except Exception as e:
            print(e)
            data = {}
        
        return data

    class Meta:
        model = User
        fields = ["type","emp_id","first_name","last_name","email","employee_details"]