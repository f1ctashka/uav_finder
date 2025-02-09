from feedback.views import FeedbackViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", FeedbackViewSet, basename="feedback")

urlpatterns = [*router.urls]
