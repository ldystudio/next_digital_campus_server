from rest_framework_tracking.models import APIRequestLog

from common.permissions import IsAdminUser
from common.serializer.log import (
    APIRequestLogSerializer,
    APIRequestResponseLogSerializer,
    APIRequestErrorsLogSerializer,
)
from common.viewsets import (
    ReadOnlyModelViewSetFormatResult,
    RetrieveModelViewSetFormatResult,
)


class APIRequestLogViewSet(ReadOnlyModelViewSetFormatResult):
    queryset = APIRequestLog.objects.all().order_by("-id")
    serializer_class = APIRequestLogSerializer
    permission_classes = (IsAdminUser,)
    filterset_fields = ("username_persistent",)


class APIRequestLogResponseLogViewSet(RetrieveModelViewSetFormatResult):
    queryset = APIRequestLog.objects.values("id", "response").order_by("-id")
    serializer_class = APIRequestResponseLogSerializer
    permission_classes = (IsAdminUser,)


class APIRequestLogErrorsLogViewSet(RetrieveModelViewSetFormatResult):
    queryset = APIRequestLog.objects.values("id", "errors").order_by("-id")
    serializer_class = APIRequestErrorsLogSerializer
    permission_classes = (IsAdminUser,)
