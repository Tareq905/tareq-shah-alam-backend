# pyrefly: ignore [missing-import]
from rest_framework.views import APIView
# pyrefly: ignore [missing-import]
from rest_framework.response import Response
from .models import SiteSetting, BackgroundMusic
from .serializers import SiteSettingSerializer

class SiteSettingView(APIView):
    def get(self, request):
        setting, _ = SiteSetting.objects.get_or_create(pk=1)
        data = SiteSettingSerializer(setting, context={"request": request}).data
        bgm = BackgroundMusic.objects.order_by("-updated_at").first()
        if bgm:
            data["is_bgm_enabled"] = bool(setting.is_bgm_enabled and bgm.is_active)
            if bgm.audio_file:
                data["bgm_file"] = request.build_absolute_uri(bgm.audio_file.url)
            if bgm.title:
                data["bgm_title"] = bgm.title
        else:
            data["is_bgm_enabled"] = bool(setting.is_bgm_enabled)
        return Response(data)
