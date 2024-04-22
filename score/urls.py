from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router = SimpleRouter()
router.register(
    "information", views.ScoreInformationViewSet, basename="ScoreInformation"
)
router.register("query", views.ScoreQueryViewSet, basename="ScoreQuery")

urlpatterns = [
    path(
        "peacetime/",
        views.PeacetimeScoreListView.as_view(),
        name="PeacetimeScore",
    ),
    path(
        "ai-advise/",
        views.ScoreAIAdviseView.as_view(),
        name="ScoreAIAdvise",
    ),
] + router.urls
