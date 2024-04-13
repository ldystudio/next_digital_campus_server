from rest_framework.generics import get_object_or_404

from common.permissions import IsAdminOrTeacherUser
from common.utils.decide import is_admin
from common.viewsets import ReadOnlyModelViewSetFormatResult
from teacher.models import Information as TeacherInformation
from .models import Information
from .serializers import ClassInformationSerializer


# Create your views here.
class ClassInformationViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = ClassInformationSerializer
    permission_classes = (IsAdminOrTeacherUser,)

    def get_queryset(self):
        queryset = super().get_queryset()

        if self.action == "list" and not is_admin(self.request):
            teacher = get_object_or_404(TeacherInformation, user=self.request.user)
            return queryset.filter(id__in=teacher.classes.values_list("id", flat=True))

        return queryset
