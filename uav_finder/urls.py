from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/uavs/", include("uav.urls")),
    path("api/feedbacks/", include("feedback.urls")),
]
