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

    def __str__(self):
        return f"{self.full_name} — Site Settings"


class BackgroundMusic(SiteSetting):
    """
    Dedicated Proxy model to expose BGM as a direct, standalone menu item in Django Admin.
    """
    class Meta:
        proxy = True
        verbose_name = "Background Music (BGM)"
        verbose_name_plural = "Background Music (BGM)"

