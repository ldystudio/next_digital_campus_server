from common.result import Result
from common.viewsets import ModelViewSetFormatResult
from .filters import CourseSettingFilter
from .models import Setting
from .serializers import CourseSettingSerializer


# Create your views here.
class CourseSettingsViewSet(ModelViewSetFormatResult):
    queryset = Setting.objects.all()
    serializer_class = CourseSettingSerializer
    filterset_class = CourseSettingFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        # 获取请求中的教师 ID 列表
        teacher_ids = request.data.get("teacher", [])
        # 在保存课程之前，将教师列表中的教师 ID 添加到课程的教师列表中
        instance.teacher.set(teacher_ids)
        self.perform_update(serializer)
        return Result.OK_202_ACCEPTED(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 获取请求中的教师 ID 列表
        teacher_ids = request.data.get("teacher", [])
        # 在保存课程之前，将教师列表中的教师 ID 添加到课程的教师列表中
        serializer.save(teacher=teacher_ids)
        return Result.OK_201_CREATED(data=serializer.data)
