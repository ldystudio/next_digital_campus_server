from common.permissions import IsOwnerOperation, IsAdminOrTeacherUser
from common.viewsets import ModelViewSetFormatResult
from .models import Enter
from .serializers import ScoreEnterSerializer


# Create your views here.
class ScoreEnterViewSet(ModelViewSetFormatResult):
    queryset = Enter.objects.all().distinct()
    serializer_class = ScoreEnterSerializer
    permission_classes = (
        IsAdminOrTeacherUser,
        IsOwnerOperation,
    )

    # filterset_class = CourseSettingFilter

    # def list(self, request, *args, **kwargs):
    #     if is_admin(request):
    #         return super().list(request, *args, **kwargs)
