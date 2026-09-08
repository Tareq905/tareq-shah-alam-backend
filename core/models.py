import os
from django.db import models
from django.core.exceptions import ValidationError

def validate_bgm_file(file):
    """
    Validates that the uploaded audio file is a valid audio format and does not exceed 100MB.
    """
    valid_extensions = [".mp3", ".wav", ".ogg", ".m4a", ".aac"]
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f"Unsupported audio format '{ext}'. Allowed formats: {', '.join(valid_extensions)}"
        )
    
    max_size = 100 * 1024 * 1024  # 100 MB
    if file.size > max_size:
        raise ValidationError(
            f"File size exceeds 100 MB limit ({file.size / (1024 * 1024):.1f} MB uploaded)."
        )

class SiteSetting(models.Model):
    full_name = models.CharField(max_length=150, default="Md Tareq Shah Alam")
    headline = models.CharField(max_length=255, default="Machine Learning Engineer & Data Scientist")
    bio = models.TextField(
        default="Passionate about extracting actionable insights from data and architecting cutting-edge AI solutions. Specializing in NLP, Transformers, CNNs, LangChain, LlamaIndex, and advanced SQL workflows to solve complex real-world challenges."
    )
    email = models.EmailField(default="tareqshah.027@gmail.com")
    whatsapp_number = models.CharField(
        max_length=50,
        default="+8801625801530",
        help_text="Phone number with country code for Talk with me button"
    )
    location = models.CharField(max_length=150, default="Dhaka, Bangladesh")
    
    # Links
    blog_url = models.URLField(
        default="https://medium.com/@tareqshahalam",
        help_text="Blog / Medium / Articles URL for 'Read Articles' buttons"
    )
    github_url = models.URLField(default="https://github.com/tareqshah027", blank=True)
    linkedin_url = models.URLField(default="https://www.linkedin.com/in/md-tareq-shah-alam/", blank=True)
    kaggle_url = models.URLField(default="https://www.kaggle.com", blank=True)
    twitter_url = models.URLField(default="https://twitter.com", blank=True)
    resume_url = models.URLField(blank=True, default="")
    
    # Background Music (BGM) Configuration
    is_bgm_enabled = models.BooleanField(
        default=True,
        verbose_name="Enable Background Music (BGM)",
        help_text="Uncheck to pause / silence music portfolio-wide."
    )
    bgm_file = models.FileField(
        upload_to="bgm/",
        blank=True,
        null=True,
        validators=[validate_bgm_file],
        verbose_name="Custom BGM Audio File (MP3, Max 100MB)",
        help_text="Upload custom MP3 audio (up to 100MB). To switch back to default, simply clear/delete this file."
    )
    bgm_title = models.CharField(
        max_length=150,
        blank=True,
        default="Arabic Ambient BGM",
        verbose_name="BGM Title / Track Name",
        help_text="Name of the currently active background track"
    )
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Configuration"
        verbose_name_plural = "Site Configuration"

    def save(self, *args, **kwargs):
        # Enforce singleton pattern (only 1 config object)
        self.pk = 1
        super().save(*args, **kwargs)
        # Keep BackgroundMusic model in sync
        try:
            BackgroundMusic.objects.all().update(is_active=self.is_bgm_enabled)
        except Exception:
            pass

    def __str__(self):
        return f"{self.full_name} — Site Settings"


class BackgroundMusic(models.Model):
    """
    Dedicated Background Music management model with MP3 file upload up to 100MB,
    pause/play toggle, and default fallback.
    """
    title = models.CharField(
        max_length=200,
        default="Background Music Track",
        verbose_name="Track Title",
        help_text="Title or description of the background music"
    )
    audio_file = models.FileField(
        upload_to="bgm/",
        blank=True,
        null=True,
        validators=[validate_bgm_file],
        verbose_name="Upload MP3 File (Max 100MB)",
        help_text="Upload custom MP3 audio (up to 100MB). When uploaded, this plays as base BGM. Delete/clear file to play default arabic-bgm.mp3."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Play / Enable Music",
        help_text="Uncheck to pause/silence music portfolio-wide."
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Background Music (BGM)"
        verbose_name_plural = "Background Music (BGM)"
        ordering = ["-updated_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Keep SiteSetting in sync
        try:
            SiteSetting.objects.filter(pk=1).update(is_bgm_enabled=self.is_active)
        except Exception:
            pass

    def __str__(self):
        status = "PLAYING" if self.is_active else "PAUSED"
        source = "Custom Upload" if self.audio_file else "Default arabic-bgm.mp3"
        return f"{self.title} [{status} • {source}]"


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=SiteSetting)
def sync_bgm_from_sitesetting(sender, instance, **kwargs):
    try:
        BackgroundMusic.objects.all().update(is_active=instance.is_bgm_enabled)
    except Exception:
        pass

@receiver(post_save, sender=BackgroundMusic)
def sync_sitesetting_from_bgm(sender, instance, **kwargs):
    try:
        SiteSetting.objects.filter(pk=1).update(is_bgm_enabled=instance.is_active)
    except Exception:
        pass

