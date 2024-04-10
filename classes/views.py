from rest_framework_extensions.cache.decorators import cache_response

from common.result import Result
from common.utils.decide import is_admin, is_teacher
from common.viewsets import ReadOnlyModelViewSetFormatResult
from teacher.models import Information as TeacherInformation
from .models import Information
from .serializers import ClassInformationSerializer


# Create your views here.
class ClassInformationViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = ClassInformationSerializer

    @cache_response(key_func="list_cache_key_func")
    def list(self, request, *args, **kwargs):
        if is_admin(request):
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(
                self.paginate_queryset(queryset), many=True
            )
            paginated_response = self.get_paginated_response(serializer.data)
            return Result.OK_200_SUCCESS(data=paginated_response.data)
        elif is_teacher(request):
            teacher = TeacherInformation.objects.get(user=request.user)
            queryset = self.filter_queryset(
                self.get_queryset().filter(
                    id__in=teacher.classes.values_list("id", flat=True)
                )
            )
            serializer = self.get_serializer(
                self.paginate_queryset(queryset), many=True
            )
            paginated_response = self.get_paginated_response(serializer.data)
            return Result.OK_200_SUCCESS(data=paginated_response.data)
