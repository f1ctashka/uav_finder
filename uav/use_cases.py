from uav.exceptions import UAVNotFoundError, UAVTypeNotFoundError
from uav.models import UAV, UAVType, Coordinate
from uav.utils import encrypt
from users.models import User


class CreateUAVUseCaseImpl:
    def __call__(
        self,
        serial_number: str,
        model_type_id: int,
        max_speed: int,
        max_height: int,
        owner: User,
        users: list[int],
        icloud_login: str | None = None,
        icloud_password: str | None = None,
        coordinates: list[dict[str, float]] | None = None,
    ) -> None:
        try:
            UAVType.objects.get(id=model_type_id)
        except UAVType.DoesNotExist:
            raise UAVTypeNotFoundError

        uav = UAV.objects.create(
            serial_number=serial_number,
            model_type_id=model_type_id,
            max_speed=max_speed,
            max_height=max_height,
            owner=owner,
            icloud_login=icloud_login,
        )
        if icloud_password:
            uav.icloud_password = encrypt(icloud_password.encode()).decode()
            uav.save(update_fields=("icloud_password",))

        if users:
            uav.users.set(users)

        if coordinates:
            Coordinate.objects.bulk_create(
                Coordinate(uav_id=uav.id, **coord) for coord in coordinates
            )


class ListUAVUseCaseImpl:
    def __call__(self, user: User) -> list[UAV]:
        return (
            UAV.objects.select_related("owner")
            .prefetch_related("coordinates")
            .filter(owner=user)
        )


class GetUAVUseCaseImpl:
    def __call__(self, uav_id: int, user: User) -> UAV:
        uavs = UAV.objects.select_related("owner")
        if not user.is_staff:
            uavs = uavs.filter(owner=user)

        try:
            return uavs.get(id=uav_id)
        except UAV.DoesNotExist:
            raise UAVNotFoundError


class UpdateUAVUseCaseImpl:
    def __call__(
        self,
        uav_id: int,
        serial_number: str,
        model_type_id: int,
        max_speed: int,
        max_height: int,
        owner: User,
        users: list[int],
        icloud_login: str | None = None,
        icloud_password: str | None = None,
        coordinates: list[dict[str, float]] | None = None,
    ) -> UAV:
        uavs = UAV.objects.select_related("owner")
        if not owner.is_staff:
            uavs = uavs.filter(owner=owner)

        try:
            uav = uavs.get(id=uav_id)
        except UAV.DoesNotExist:
            raise UAVNotFoundError

        try:
            UAVType.objects.get(id=model_type_id)
        except UAVType.DoesNotExist:
            raise UAVTypeNotFoundError

        uav.serial_number = serial_number
        uav.model_type_id = model_type_id
        uav.max_speed = max_speed
        uav.max_height = max_height
        uav.save(
            update_fields=("serial_number", "model_type", "max_speed", "max_height")
        )

        if icloud_password:
            uav.icloud_password = encrypt(icloud_password.encode()).decode()
            uav.save(update_fields=("icloud_password",))

        if users:
            uav.users.set(users)

        if coordinates:
            uav.coordinates.all().delete()
            Coordinate.objects.bulk_create(
                Coordinate(uav_id=uav_id, **coord) for coord in coordinates
            )

        return uav
