from django.db import models

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
