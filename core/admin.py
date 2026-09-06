from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSetting, BackgroundMusic

@admin.register(BackgroundMusic)
class BackgroundMusicAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "audio_file", "audio_player", "updated_at")
    list_editable = ("is_active",)
    readonly_fields = ("audio_player",)
    fields = ("title", "is_active", "audio_file", "audio_player")

    def audio_player(self, obj):
        if obj and obj.audio_file:
            return format_html(
                '<audio controls src="{}" style="height: 38px; vertical-align: middle;"></audio>',
                obj.audio_file.url
            )
        return format_html(
            '<span style="color: #06b6d4; font-family: monospace; font-size: 13px; font-weight: 600;">'
            '🎵 Default Base Track: <code>/arabic-bgm.mp3</code> (Active)'
            '</span>'
        )
    audio_player.short_description = "Live Audio Player / Test"


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
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)
