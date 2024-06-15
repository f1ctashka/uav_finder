from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from users.exceptions import UserHasNoPermissionError, UserNotFoundError
from users.serializers import (
    RegisterUserInputSerializer,
    ResetPasswordInputSerializer,
    UserOutputSerializer,
    UserUpdateInputSerializer,
)
from users.use_cases import (
    RegisterUserUseCaseImpl,
    ResetPasswordUseCaseImpl,
    RetrieveUserUseCaseImpl,
    UpdateUserUseCaseImpl,
)


class UserViewSet(ViewSet):
    lookup_value_regex = r"\d+"

    def retrieve(self, request: Request, pk: int) -> Response:
        use_case = RetrieveUserUseCaseImpl()
        try:
            user = use_case(user_id=int(pk), user=request.user)
        except UserNotFoundError:
            raise NotFound
        except UserHasNoPermissionError:
            raise PermissionDenied

        output_serializer = UserOutputSerializer(instance=user)
        return Response(output_serializer.data)

    def update(self, request: Request, pk: int) -> Response:
        input_serializer = UserUpdateInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        use_case = UpdateUserUseCaseImpl()
        try:
            user = use_case(
                user_id=int(pk),
                data=input_serializer.validated_data,
                user=request.user,
            )
        except UserNotFoundError:
            raise NotFound
        except UserHasNoPermissionError:
            raise PermissionDenied
        except ValueError as e:
            raise ValidationError(str(e))

        output_serializer = UserOutputSerializer(instance=user)
        return Response(output_serializer.data)

    @action(detail=False, methods=["POST"], permission_classes=(AllowAny,))
    def register(self, request: Request) -> Response:
        input_serializer = RegisterUserInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        use_case = RegisterUserUseCaseImpl()
        try:
            use_case(
                username=input_serializer.validated_data["username"],
                email=input_serializer.validated_data["email"],
                password=input_serializer.validated_data["password"],
            )
        except ValueError as e:
            raise ValidationError(str(e))
        return Response()

    @action(detail=False, methods=["POST"], permission_classes=(AllowAny,))
    def reset_password(self, request: Request) -> Response:
        input_serializer = ResetPasswordInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        use_case = ResetPasswordUseCaseImpl()
        try:
            use_case(
                email=input_serializer.validated_data["email"],
                password1=input_serializer.validated_data["password1"],
                password2=input_serializer.validated_data["password2"],
            )
        except ValueError as e:
            raise ValidationError(str(e))
        return Response()
