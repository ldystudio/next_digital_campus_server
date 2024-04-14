from common.permissions import IsTeacherOrAdminUser
from common.utils.decide import is_teacher
from common.viewsets import ReadOnlyModelViewSetFormatResult
from .models import Information
from .serializers import ClassInformationSerializer


# Create your views here.
class ClassInformationViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = ClassInformationSerializer
    permission_classes = (IsTeacherOrAdminUser,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list" and is_teacher(self.request):
            return queryset.filter(teacher=self.request.user.teacher)

        return queryset
