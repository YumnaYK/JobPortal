from django.core.exceptions import ValidationError

def validate_file_size(value):
    limit = 8 * 1024 * 1024  # 8 MB

    if value.size > limit:
        raise ValidationError(f"File size cannot exceed {limit} bytes.")