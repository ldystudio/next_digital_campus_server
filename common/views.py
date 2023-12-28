from rest_framework_tracking.models import APIRequestLog

from common.permissions import IsAdminUser
from common.serializer import APIRequestLogSerializer
from common.viewsets import ReadOnlyModelViewSetWithResult


class APIRequestLogViewSet(ReadOnlyModelViewSetWithResult):
    queryset = APIRequestLog.objects.all()
    serializer_class = APIRequestLogSerializer
    permission_classes = (IsAdminUser,)
