from django.contrib import admin
from .models import SiteSetting

@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "headline",
        "is_bgm_enabled",
        "bgm_title",
        "bgm_file",
        "whatsapp_number",
        "email",
        "updated_at",
    )
    list_editable = ("is_bgm_enabled",)
    fieldsets = (
        ("Personal & Branding Info", {
            "fields": ("full_name", "headline", "bio", "location")
        }),
        ("Background Music (BGM) Control Center", {
            "fields": ("is_bgm_enabled", "bgm_file", "bgm_title"),
            "description": (
                "🎵 <strong>Music Control:</strong><br>"
                "• <strong>Enable BGM:</strong> Check to play music, uncheck to pause/mute music everywhere.<br>"
                "• <strong>Custom BGM Audio:</strong> Upload your custom MP3 file (Maximum size: 100 MB).<br>"
                "• <strong>Revert to Default:</strong> To use default <code>arabic-bgm.mp3</code>, simply clear / delete the uploaded file."
            )
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
