from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "ai_badge", "is_read", "is_spam", "created_at")
    list_filter = ("is_read", "is_spam", "ai_validation_status", "created_at")
    search_fields = ("name", "email", "subject", "message", "ai_analysis_notes")
    list_editable = ("is_read", "is_spam")
    readonly_fields = ("name", "email", "subject", "message", "ai_validation_status", "ai_analysis_notes", "ip_address", "created_at")
    actions = ["mark_as_read", "mark_as_unread", "mark_as_spam"]

    def ai_badge(self, obj):
        if obj.ai_validation_status == "GENUINE":
            return mark_safe(
                '<span style="background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid #10b981; padding: 3px 8px; border-radius: 9999px; font-weight: bold; font-size: 11px;">✓ Genuine</span>'
            )
        elif obj.ai_validation_status == "BLOCKED_DISPOSABLE":
            return mark_safe(
                '<span style="background: rgba(239, 68, 68, 0.2); color: #ef4444; border: 1px solid #ef4444; padding: 3px 8px; border-radius: 9999px; font-weight: bold; font-size: 11px;">✕ Disposable/Fake</span>'
            )
        return mark_safe(
            '<span style="background: rgba(245, 158, 11, 0.2); color: #f59e0b; border: 1px solid #f59e0b; padding: 3px 8px; border-radius: 9999px; font-weight: bold; font-size: 11px;">⚠ Suspicious</span>'
        )
    ai_badge.short_description = "AI Authenticity"

    @admin.action(description="Mark selected messages as Read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected messages as Unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)

    @admin.action(description="Mark selected messages as Spam")
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True)
