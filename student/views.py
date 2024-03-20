from common.permissions import IsOwnerOperation, IsAdminUser
from common.result import Result
from common.viewsets import ModelViewSetFormatResult
from .filters import StudentInformationFilter
from .models import Information
from .serializers import StudentInformationSerializer
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from iam.models import User


# Create your views here.
class StudentInformationViewSet(ModelViewSetFormatResult):
    queryset = Information.objects.all()
    serializer_class = StudentInformationSerializer
    permission_classes = (IsOwnerOperation,)
    filter_backends = (OrderingFilter, filters.DjangoFilterBackend)
    filterset_class = StudentInformationFilter

    def get_permissions(self):
        # 仅对“list”操作应用IsAdminUser权限
        return (IsAdminUser(),) if self.action == "list" else super().get_permissions()

    def create(self, request, *args, **kwargs):
        return Result.FAIL_403_NO_PERMISSION(msg="不支持POST请求")

    def split_data(self, request_data):
        user_data = {}
        information_data = {}
        for key, value in request_data.items():
            if key in ["real_name", "phone", "email", "avatar"]:
                user_data[key] = value
            elif key in self.serializer_class().get_fields():
                information_data[key] = value
        return user_data, information_data

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = User.objects.get(id=instance.user_id)
        except (User.DoesNotExist, Information.DoesNotExist):
            return Result.FAIL_404_NOT_FOUND(msg="用户或信息不存在")

        user_data, information_data = self.split_data(request.data)

        # 判断并更新User表
        if user_data:
            for attr, val in user_data.items():
                setattr(user, attr, val)
            user.save()

        # 判断并更新Information表
        if information_data:
            for attr, val in information_data.items():
                setattr(instance, attr, val)
            instance.save()

        serializer = self.get_serializer(instance)
        return Result.OK_202_ACCEPTED(data=serializer.data)
