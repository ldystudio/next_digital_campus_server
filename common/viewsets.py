from rest_framework.viewsets import ModelViewSet
from rest_framework_tracking.mixins import LoggingMixin

from common.result import Result


class ModelViewSetWithResult(LoggingMixin, ModelViewSet):
    logging_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Result.OK_200_SUCCESS(data=response.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Result.OK_201_CREATED(data=response.data)

    # def update(self, request, *args, **kwargs):
    #     response = super().update(request, *args, **kwargs)
    #     return Result.OK_202_ACCEPTED(data=response.data)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        return Result.OK_202_ACCEPTED(data=response.data)

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        return Result.OK_204_NO_CONTENT(data=response.data)
