from rest_framework.views import APIView
from rest_framework.response import Response
from .models import SiteSetting
from .serializers import SiteSettingSerializer

class SiteSettingView(APIView):
    def get(self, request):
        setting, _ = SiteSetting.objects.get_or_create(pk=1)
        serializer = SiteSettingSerializer(setting)
        return Response(serializer.data)
