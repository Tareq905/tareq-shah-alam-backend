from django.db import models

class Education(models.Model):
    degree = models.CharField(max_length=200, help_text="e.g. B.Sc. in Computer Science & Engineering / M.Sc.")
    institution = models.CharField(max_length=255, help_text="e.g. University Name / College")
    location = models.CharField(max_length=150, default="Dhaka, Bangladesh")
    start_year = models.CharField(max_length=50, default="2020")
    end_year = models.CharField(max_length=50, default="2024", help_text="e.g. 2024 or Present")
    grade_or_cgpa = models.CharField(max_length=100, blank=True, default="", help_text="e.g. CGPA: 3.85 / 4.00")
    field_of_study = models.CharField(max_length=255, blank=True, default="Computer Science & Data Science")
    thesis_or_description = models.TextField(
        blank=True,
        default="",
        help_text="Key coursework, thesis topic, or research accomplishments"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Education"
        verbose_name_plural = "Education"

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Experience(models.Model):
    role = models.CharField(max_length=200, help_text="e.g. Machine Learning Engineer / AI Researcher")
    company = models.CharField(max_length=200, help_text="e.g. AI Research Lab / Company Name")
    period = models.CharField(max_length=100, default="2024 - Present")
    location = models.CharField(max_length=150, default="Remote / Dhaka")
    job_type = models.CharField(max_length=100, default="Full-Time / Research", blank=True)
    description = models.TextField(help_text="Key accomplishments and impact in this role")
    technologies = models.CharField(
        max_length=500,
        default="PyTorch, Transformers, LangChain, Python",
        help_text="Comma-separated list of tools used"
    )
    order = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Experience / Job"
        verbose_name_plural = "Experiences & Jobs"

    def __str__(self):
        return f"{self.role} at {self.company}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ("Applied AI & ML", "Applied AI & ML"),
        ("NLP & LLMs", "NLP & LLMs"),
        ("Computer Vision", "Computer Vision"),
        ("Data Engineering", "Data Engineering"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default="Applied AI & ML")
    image_url = models.CharField(
        max_length=500,
        blank=True,
        default="/projects/project1.png",
        help_text="Local path e.g. /projects/project1.png or full web URL"
    )
    image_file = models.ImageField(upload_to="projects/", blank=True, null=True, help_text="Or upload an image")
    live_url = models.URLField(blank=True, default="", help_text="Live demo or paper demo URL")
    github_url = models.URLField(blank=True, default="", help_text="GitHub repository URL")
    tech_stack = models.CharField(
        max_length=500,
        default="PyTorch, Transformers, FastAPI, Docker",
        help_text="Comma-separated technologies"
    )
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def get_image(self, request=None):
        if self.image_file:
            try:
                url = self.image_file.url
                if request:
                    return request.build_absolute_uri(url)
                return url
            except Exception:
                pass
        return self.image_url or "/projects/project1.png"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image_file:
            try:
                if not self.image_url or self.image_url.startswith("/projects/"):
                    Project.objects.filter(pk=self.pk).update(image_url=self.image_file.url)
            except Exception:
                pass

    def __str__(self):
        return self.title


class ResearchPaper(models.Model):
    title = models.CharField(max_length=300)
    publisher = models.CharField(max_length=200, default="arXiv / IEEE", help_text="e.g. arXiv / IEEE / Springer")
    publication_date = models.CharField(max_length=100, default="2025")
    abstract = models.TextField()
    paper_url = models.URLField(blank=True, default="", help_text="Link to paper website / DOI")
    pdf_url = models.URLField(blank=True, default="", help_text="Direct link to PDF download")
    tags = models.CharField(
        max_length=400,
        default="Deep Learning, NLP, Transformers",
        help_text="Comma-separated tags"
    )
    citations_count = models.PositiveIntegerField(default=0, blank=True)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Research Paper"
        verbose_name_plural = "Research & Papers"

    def __str__(self):
        return self.title
