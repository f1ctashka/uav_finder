from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from uav.exceptions import UAVNotFoundError
from uav.serializers import CreateUpdateUAVInputSerializer, UAVOutputSerializer
from uav.use_cases import (
    CreateUAVUseCaseImpl,
    GetUAVUseCaseImpl,
    ListUAVUseCaseImpl,
    UpdateUAVUseCaseImpl,
)


class UAVViewSet(ViewSet):
    lookup_value_regex = r"\d+"

    def create(self, request: Request) -> Response:
        input_serializer = CreateUpdateUAVInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        use_case = CreateUAVUseCaseImpl()
        use_case(
            max_speed=input_serializer.validated_data["max_speed"],
            max_height=input_serializer.validated_data["max_height"],
            model_type_id=input_serializer.validated_data["model_type_id"],
            serial_number=input_serializer.validated_data["serial_number"],
            owner=request.user,
            icloud_login=input_serializer.validated_data.get("icloud_login"),
            icloud_password=input_serializer.validated_data.get("icloud_password"),
            users=input_serializer.validated_data["users"],
            coordinates=input_serializer.validated_data["coordinates"],
        )
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request: Request) -> Response:
        use_case = ListUAVUseCaseImpl()
        uavs = use_case(user=request.user)

        output_serializer = UAVOutputSerializer(uavs, many=True)
        return Response(output_serializer.data)

    def retrieve(self, request: Request, pk: int) -> Response:
        use_case = GetUAVUseCaseImpl()

        try:
            uav = use_case(uav_id=int(pk), user=request.user)
        except UAVNotFoundError:
            raise NotFound

        output_serializer = UAVOutputSerializer(uav)
        return Response(output_serializer.data)

    def update(self, request: Request, pk: int) -> Response:
        input_serializer = CreateUpdateUAVInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        use_case = UpdateUAVUseCaseImpl()
        try:
            uav = use_case(
                uav_id=int(pk),
                max_speed=input_serializer.validated_data["max_speed"],
                max_height=input_serializer.validated_data["max_height"],
                model_type_id=input_serializer.validated_data["model_type_id"],
                serial_number=input_serializer.validated_data["serial_number"],
                owner=request.user,
                users=input_serializer.validated_data["users"],
                coordinates=input_serializer.validated_data["coordinates"],
                icloud_login=input_serializer.validated_data.get("icloud_login"),
                icloud_password=input_serializer.validated_data.get("icloud_password"),
            )
        except UAVNotFoundError:
            raise NotFound

        output_serializer = UAVOutputSerializer(uav)
        return Response(output_serializer.data)
