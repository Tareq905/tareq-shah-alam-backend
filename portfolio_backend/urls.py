from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core.views import SiteSettingView
from portfolio.views import (
    EducationListView,
    ExperienceListView,
    ProjectListView,
    ResearchPaperListView,
    PortfolioBundleView,
)
from contacts.views import ContactSubmitView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Core & Site Configuration API
    path("api/site-settings/", SiteSettingView.as_view(), name="site-settings"),

    # Portfolio Dynamic APIs
    path("api/education/", EducationListView.as_view(), name="education-list"),
    path("api/experience/", ExperienceListView.as_view(), name="experience-list"),
    path("api/projects/", ProjectListView.as_view(), name="projects-list"),
    path("api/research/", ResearchPaperListView.as_view(), name="research-list"),
    path("api/all/", PortfolioBundleView.as_view(), name="portfolio-bundle"),

    # Contact & AI Guard API
    path("api/contact/", ContactSubmitView.as_view(), name="contact-submit"),
]

from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
