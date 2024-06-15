from django.db import models


class UAVType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class UAV(models.Model):
    class Status(models.TextChoices):
        active = "active"
        inactive = "inactive"

    serial_number = models.CharField(max_length=100)
    model_type = models.ForeignKey(
        UAVType, on_delete=models.CASCADE, related_name="uavs"
    )
    max_speed = models.IntegerField()
    max_height = models.IntegerField()
    status = models.CharField(
        max_length=8, choices=Status.choices, default=Status.active
    )
    owner = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="owned_uavs"
    )
    icloud_login = models.CharField(max_length=255, blank=True, null=True)
    icloud_password = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField("users.User", related_name="uavs", blank=True)

    @property
    def owner_username(self) -> str:
        return self.owner.username

    def __str__(self) -> str:
        return self.serial_number


class Coordinate(models.Model):
    uav = models.ForeignKey(UAV, on_delete=models.CASCADE, related_name="coordinates")
    latitude = models.FloatField()
    longitude = models.FloatField()
