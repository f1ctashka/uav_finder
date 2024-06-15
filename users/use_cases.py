from typing import Any

from django.db import IntegrityError
from users.exceptions import UserHasNoPermissionError, UserNotFoundError
from users.models import User


class RegisterUserUseCaseImpl:
    def __call__(self, username: str, email: str, password: str) -> None:
        try:
            User.objects.create_user(username=username, email=email, password=password)
        except IntegrityError as e:
            raise ValueError(e)


class ResetPasswordUseCaseImpl:
    def __call__(self, email: str, password1: str, password2: str) -> None:
        if password1 != password2:
            raise ValueError("Passwords do not match")
        user = User.objects.get(email=email)
        user.set_password(password1)
        user.save()


class RetrieveUserUseCaseImpl:
    def __call__(self, user_id: int, user: User) -> User:
        if not user.is_staff and user.id != user_id:
            raise UserHasNoPermissionError

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundError


class UpdateUserUseCaseImpl:
    def __call__(self, user_id: int, user: User, data: dict[str, Any]) -> User:
        if not user.is_staff and any([user.id != user_id, "is_staff" in data]):
            raise UserHasNoPermissionError

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundError

        for key, value in data.items():
            setattr(user, key, value)

        try:
            user.save()
        except IntegrityError as e:
            raise ValueError(e)

        user.refresh_from_db()
        return user
