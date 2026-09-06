from django.contrib import admin
from django.utils.html import format_html
from .models import Education, Experience, Project, ResearchPaper

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("degree", "institution", "start_year", "end_year", "grade_or_cgpa", "order", "is_active")
    list_filter = ("is_active", "start_year", "end_year")
    search_fields = ("degree", "institution", "field_of_study", "thesis_or_description")
    list_editable = ("order", "is_active")
    ordering = ("order", "-created_at")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "period", "location", "job_type", "order", "is_active")
    list_filter = ("is_active", "job_type")
    search_fields = ("role", "company", "technologies", "description")
    list_editable = ("order", "is_active")
    ordering = ("order", "-created_at")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("preview_thumbnail", "title", "category", "tech_stack", "is_featured", "order", "created_at")
    list_filter = ("category", "is_featured", "created_at")
    search_fields = ("title", "description", "tech_stack")
    list_editable = ("is_featured", "order")
    ordering = ("order", "-created_at")
    readonly_fields = ("current_image_preview", "created_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "category", "description", "order", "is_featured")
        }),
        ("Project Visual / Image", {
            "fields": ("image_file", "current_image_preview", "image_url"),
            "description": "Upload a new image file (recommended) OR provide an image URL / path. Uploaded files take priority."
        }),
        ("External Links", {
            "fields": ("live_url", "github_url")
        }),
        ("Technologies & Timestamps", {
            "fields": ("tech_stack", "created_at")
        }),
    )

    def preview_thumbnail(self, obj):
        img_src = obj.get_image()
        if img_src:
            return format_html(
                '<img src="{}" style="width: 48px; height: 32px; object-fit: cover; border-radius: 4px; border: 1px solid rgba(255,255,255,0.2);" />',
                img_src
            )
        return "No Image"
    preview_thumbnail.short_description = "Preview"

    def current_image_preview(self, obj):
        if not obj or not obj.pk:
            return "Save project to view preview."
        img_src = obj.get_image()
        if img_src:
            return format_html(
                '<div style="margin: 6px 0;">'
                '<img src="{}" style="max-width: 280px; max-height: 160px; object-fit: cover; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); box-shadow: 0 4px 12px rgba(0,0,0,0.5);" />'
                '<div style="color: #00e5ff; font-size: 11px; margin-top: 4px; font-family: monospace;">Source: {}</div>'
                '</div>',
                img_src,
                img_src
            )
        return "No image uploaded yet"
    current_image_preview.short_description = "Active Image Preview"


@admin.register(ResearchPaper)
class ResearchPaperAdmin(admin.ModelAdmin):
    list_display = ("title", "publisher", "publication_date", "tags", "order", "created_at")
    list_filter = ("publisher", "publication_date")
    search_fields = ("title", "abstract", "tags", "publisher")
    list_editable = ("order",)
    ordering = ("order", "-created_at")
