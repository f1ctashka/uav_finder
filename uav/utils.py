from typing import TypedDict

from cryptography.fernet import Fernet
from django.conf import settings
from pyicloud import PyiCloudService
from pyicloud.exceptions import PyiCloudFailedLoginException


f = Fernet(settings.CRYPTOGRAPHY_KEY)


def encrypt(value: bytes) -> bytes:
    return f.encrypt(value)


def decrypt(value: bytes) -> bytes:
    return f.decrypt(value)


class Location(TypedDict):
    latitude: float
    longitude: float


def get_location(login: str, password: str) -> Location:
    api = PyiCloudService(login, password)
    try:
        location = api.devices[0].location()
    except PyiCloudFailedLoginException:
        return {
            "latitude": 0.0,
            "longitude": 0.0,
        }
    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }
