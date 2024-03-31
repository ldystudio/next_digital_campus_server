from common.viewsets import ReadOnlyModelViewSetFormatResult
from .models import Information
from .serializers import ClassInformationSerializer


# Create your views here.
class ClassInformationViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = ClassInformationSerializer
