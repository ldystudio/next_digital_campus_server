from common.permissions import IsTeacherOrAdminUser
from common.utils.decide import is_teacher, is_student
from common.viewsets import ModelViewSetFormatResult
from .filters import ScoreInformationFilter
from .models import Information
from .serializers import ScoreInformationSerializer


class ScoreInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all().distinct()
    serializer_class = ScoreInformationSerializer
    filterset_class = ScoreInformationFilter

    def get_permissions(self):
        if self.action == "create":
            return (IsTeacherOrAdminUser(),)
        return super().get_permissions()

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            if is_teacher(self.request):
                return queryset.filter(course__teacher=self.request.user.teacher)
            elif is_student(self.request):
                return queryset.filter(student=self.request.user.student)
        return queryset
