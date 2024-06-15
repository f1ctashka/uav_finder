from django.contrib import admin
from uav.models import UAV, UAVType, Coordinate


@admin.register(UAV)
class UAVAdmin(admin.ModelAdmin):
    pass


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    pass


@admin.register(UAVType)
class UAVTypeAdmin(admin.ModelAdmin):
    pass
