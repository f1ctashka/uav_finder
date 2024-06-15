from rest_framework import serializers


class CreateFeedbackInputSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
