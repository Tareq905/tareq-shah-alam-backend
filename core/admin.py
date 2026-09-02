from django.contrib import admin
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ("full_name", "headline", "whatsapp_number", "email", "blog_url", "updated_at")
    fieldsets = (
        ("Personal & Branding Info", {
            "fields": ("full_name", "headline", "bio", "location")
        }),
        ("Contact & Instant Communication", {
            "fields": ("whatsapp_number", "email")
        }),
        ("Social & External Profiles", {
            "fields": ("blog_url", "github_url", "linkedin_url", "kaggle_url", "twitter_url", "resume_url")
        }),
    )

    def has_add_permission(self, request):
        # Only allow 1 singleton instance
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
