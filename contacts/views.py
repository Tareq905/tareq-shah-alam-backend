from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactMessage
from .serializers import ContactMessageSerializer
from .validators import analyze_with_ai_guard

class ContactSubmitView(APIView):
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if not serializer.is_valid():
            # Return first clean error message
            errors = serializer.errors
            first_err = next(iter(errors.values()))[0] if errors else "Invalid submission data."
            return Response({"error": first_err, "details": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Run AI Deep Authenticity Analysis
        name = serializer.validated_data.get("name", "")
        email = serializer.validated_data.get("email", "")
        subject = serializer.validated_data.get("subject", "Collaboration Inquiry")
        message = serializer.validated_data.get("message", "")

        ai_result = analyze_with_ai_guard(name, email, subject, message)
        
        if ai_result.get("status") in ["BLOCKED", "BLOCKED_DISPOSABLE"]:
            return Response(
                {"error": ai_result.get("reason", "Submission rejected by security filters.")},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract Client IP
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        # Save verified message
        contact = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ai_validation_status=ai_result.get("status", "GENUINE"),
            ai_analysis_notes=ai_result.get("reason", "Verified genuine message."),
            is_spam=ai_result.get("is_spam", False),
            ip_address=ip,
        )

        return Response(
            {
                "success": True,
                "message": "Thank you! Your message has been verified and securely sent to Md Tareq Shah Alam.",
                "id": contact.id,
            },
            status=status.HTTP_201_CREATED
        )
