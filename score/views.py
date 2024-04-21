from common.permissions import (
    IsTeacherOrAdminUser,
    IsOwnerOperation,
    IsStudentOrAdminUser,
)
from common.utils.decide import is_admin
from common.viewsets import ModelViewSetFormatResult
from .filters import ScoreInformationFilter
from .models import Information
from .serializers import ScoreInformationSerializer, ScoreQuerySerializer


class ScoreInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreInformationSerializer
    filterset_class = ScoreInformationFilter
    permission_classes = (IsTeacherOrAdminUser, IsOwnerOperation)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if not is_admin(self.request):
                return queryset.filter(course__teacher=self.request.user.teacher)
        return queryset


class ScoreQueryViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreQuerySerializer
    filterset_class = ScoreInformationFilter
    permission_classes = (IsStudentOrAdminUser, IsOwnerOperation)

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if not is_admin(self.request):
                return queryset.filter(student=self.request.user.student)
        return queryset
