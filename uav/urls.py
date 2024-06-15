from rest_framework.routers import DefaultRouter
from uav.views import UAVViewSet


router = DefaultRouter()
router.register("", UAVViewSet, basename="uav")

urlpatterns = [*router.urls]
