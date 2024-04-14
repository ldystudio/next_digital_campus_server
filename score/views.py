from common.viewsets import ModelViewSetFormatResult
from .filters import ScoreInformationFilter
from .models import Information
from .serializers import ScoreInformationSerializer


# Create your views here.
class ScoreInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreInformationSerializer
    filterset_class = ScoreInformationFilter

    # def list(self, request, *args, **kwargs):
    #     if is_admin(request):
    #         return super().list(request, *args, **kwargs)
