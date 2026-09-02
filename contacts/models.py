from django.db import models

class ContactMessage(models.Model):
    STATUS_CHOICES = [
        ("GENUINE", "Verified Genuine"),
        ("SUSPICIOUS", "Suspicious / Review"),
        ("BLOCKED_DISPOSABLE", "Blocked Disposable/Fake"),
        ("SPAM", "Spam"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=255, default="Collaboration Inquiry")
    message = models.TextField()
    
    # Validation & AI Metadata
    is_read = models.BooleanField(default=False)
    is_spam = models.BooleanField(default=False)
    ai_validation_status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default="GENUINE"
    )
    ai_analysis_notes = models.TextField(blank=True, default="Verified by AI Gatekeeper.")
    
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.subject[:40]}"
