from rest_framework import permissions, mixins
from rest_framework.status import HTTP_201_CREATED
from rest_framework.response import Response

from take_home.views import BaseViewSet
from videos.serializers import (
    CreateVideosSerializer,
    DetailVideosSerializer,
    ResponseVideosSerializer,
)
from videos.models import VideosModel
from videos.tasks import process_video


class VideosViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, BaseViewSet):
    queryset = VideosModel.objects.all().order_by("-created_at")
    permission_classes = [
        permissions.AllowAny,
    ]
    serializer_class = CreateVideosSerializer
    create_serializer_class = CreateVideosSerializer
    retrieve_serializer_class = DetailVideosSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        process_video.delay(
            instance.id,
            file_name=instance.file_name,
            requested_rover=instance.requested_rover,
            requested_camera=instance.requested_camera,
            requested_date=instance.requested_date,
        )

    def create(self, request, *args, **kwargs):
        serializer = super().create(request, *args, **kwargs)
        return Response(
            ResponseVideosSerializer().to_representation(serializer.data),
            status=HTTP_201_CREATED,
        )
