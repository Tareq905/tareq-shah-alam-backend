from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Education, Experience, Project, ResearchPaper
from .serializers import (
    EducationSerializer,
    ExperienceSerializer,
    ProjectSerializer,
    ResearchPaperSerializer,
)
from core.models import SiteSetting, BackgroundMusic
from core.serializers import SiteSettingSerializer

class EducationListView(generics.ListAPIView):
    queryset = Education.objects.filter(is_active=True).order_by("order", "-created_at")
    serializer_class = EducationSerializer


class ExperienceListView(generics.ListAPIView):
    queryset = Experience.objects.filter(is_active=True).order_by("order", "-created_at")
    serializer_class = ExperienceSerializer


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all().order_by("order", "-created_at")
    serializer_class = ProjectSerializer


class ResearchPaperListView(generics.ListAPIView):
    queryset = ResearchPaper.objects.all().order_by("order", "-created_at")
    serializer_class = ResearchPaperSerializer


class PortfolioBundleView(APIView):
    """
    Consolidated single endpoint returning all portfolio components in 1 fast query.
    """
    def get(self, request):
        site_setting, _ = SiteSetting.objects.get_or_create(pk=1)
        education = Education.objects.filter(is_active=True).order_by("order", "-created_at")
        experience = Experience.objects.filter(is_active=True).order_by("order", "-created_at")
        projects = Project.objects.all().order_by("order", "-created_at")
        research = ResearchPaper.objects.all().order_by("order", "-created_at")

        context = {"request": request}
        site_setting_data = SiteSettingSerializer(site_setting, context=context).data

        # Determine background music configuration and active state
        bgm = BackgroundMusic.objects.order_by("-updated_at").first()
        if bgm:
            # If EITHER SiteSetting or BackgroundMusic model is toggled off, respect disable!
            site_setting_data["is_bgm_enabled"] = bool(site_setting.is_bgm_enabled and bgm.is_active)
            site_setting_data["bgm_file"] = request.build_absolute_uri(bgm.audio_file.url) if bgm.audio_file else (site_setting_data.get("bgm_file") or None)
            site_setting_data["bgm_title"] = bgm.title or site_setting.bgm_title
        else:
            site_setting_data["is_bgm_enabled"] = bool(site_setting.is_bgm_enabled)

        return Response({
            "site_setting": site_setting_data,
            "education": EducationSerializer(education, many=True, context=context).data,
            "experience": ExperienceSerializer(experience, many=True, context=context).data,
            "projects": ProjectSerializer(projects, many=True, context=context).data,
            "research": ResearchPaperSerializer(research, many=True, context=context).data,
        })
