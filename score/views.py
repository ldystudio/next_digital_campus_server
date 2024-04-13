from common.result import Result
from common.utils.decide import is_admin
from .models import Enter

from common.viewsets import ModelViewSetFormatResult
from .serializers import ScoreEnterSerializer


# Create your views here.
class ScoreEnterViewSet(ModelViewSetFormatResult):
    queryset = Enter.objects.all().distinct()
    serializer_class = ScoreEnterSerializer
    enable_cache = False

    # filterset_class = CourseSettingFilter

    def list(self, request, *args, **kwargs):
        if is_admin(request):
            return super().list(request, *args, **kwargs)
