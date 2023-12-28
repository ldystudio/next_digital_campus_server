from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register('log', views.APIRequestLogViewSet, basename='api-request-log')

urlpatterns = [
]

urlpatterns += router.urls
