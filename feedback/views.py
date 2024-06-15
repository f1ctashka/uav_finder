from feedback.serializers import CreateFeedbackInputSerializer
from feedback.use_cases import CreateFeedbackUseCaseImpl
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class FeedbackViewSet(ViewSet):
    def create(self, request: Request) -> Response:
        input_serializer = CreateFeedbackInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        use_case = CreateFeedbackUseCaseImpl()
        use_case(
            subject=input_serializer.validated_data["subject"],
            message=input_serializer.validated_data["message"],
            user=request.user,
        )

        return Response(status=status.HTTP_201_CREATED)
