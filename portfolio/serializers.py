from rest_framework import serializers
from .models import Education, Experience, Project, ResearchPaper

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"


class ExperienceSerializer(serializers.ModelSerializer):
    technologies_list = serializers.SerializerMethodField()

    class Meta:
        model = Experience
        fields = "__all__"

    def get_technologies_list(self, obj):
        if not obj.technologies:
            return []
        return [t.strip() for t in obj.technologies.split(",") if t.strip()]


class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    tech_stack_list = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = "__all__"

    def get_image(self, obj):
        return obj.get_image()

    def get_tech_stack_list(self, obj):
        if not obj.tech_stack:
            return []
        return [t.strip() for t in obj.tech_stack.split(",") if t.strip()]


class ResearchPaperSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = ResearchPaper
        fields = "__all__"

    def get_tags_list(self, obj):
        if not obj.tags:
            return []
        return [t.strip() for t in obj.tags.split(",") if t.strip()]
