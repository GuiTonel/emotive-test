from django.core.exceptions import ValidationError
from rest_framework import serializers

from videos.models import VideosModel
from videos.exceptios import VideoProcessingError


class CreateVideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideosModel
        fields = ["requested_rover", "requested_camera", "requested_date", "id"]
        read_only_fields = ["id"]


class DetailVideosSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    file = serializers.FileField()

    class Meta:
        model = VideosModel
        fields = ["file", "status"]
        read_only_fields = fields

    def get_status(self, instance):
        if instance.is_done:
            return "Done"

        return "Not Ready"

    def to_representation(self, instance):
        if instance.has_error:
            raise VideoProcessingError

        representation = super().to_representation(instance)
        if not instance.is_done:
            representation["file"] = ""

        return representation


class ResponseVideosSerializer(serializers.ModelSerializer):
    video_id = serializers.UUIDField(read_only=True, source="id")

    class Meta:
        model = VideosModel
        fields = ("video_id",)
        read_only_fields = fields
