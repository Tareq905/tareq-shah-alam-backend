from rest_framework import serializers
from .models import ContactMessage
from .validators import validate_name_authenticity, validate_email_authenticity

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ["id", "name", "email", "subject", "message", "created_at"]

    def validate_name(self, value):
        is_valid, err_msg = validate_name_authenticity(value)
        if not is_valid:
            raise serializers.ValidationError(err_msg)
        return value.strip()

    def validate_email(self, value):
        is_valid, err_msg = validate_email_authenticity(value)
        if not is_valid:
            raise serializers.ValidationError(err_msg)
        return value.strip().lower()
