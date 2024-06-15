from rest_framework import serializers


class CoordinateSerializer(serializers.Serializer):
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class CreateUpdateUAVInputSerializer(serializers.Serializer):
    serial_number = serializers.CharField(max_length=100)
    model_type_id = serializers.IntegerField(min_value=1)
    max_speed = serializers.IntegerField(min_value=0)
    max_height = serializers.IntegerField(min_value=0)
    icloud_login = serializers.CharField(max_length=255, required=False)
    icloud_password = serializers.CharField(max_length=255, required=False)
    users = serializers.ListField(child=serializers.IntegerField(), allow_empty=True)
    coordinates = CoordinateSerializer(many=True)


class UAVTypeOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class UAVOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    serial_number = serializers.CharField()
    model_type = UAVTypeOutputSerializer()
    max_speed = serializers.IntegerField()
    max_height = serializers.IntegerField()
    status = serializers.CharField()
    owner_username = serializers.CharField()
    coordinates = CoordinateSerializer(many=True)
