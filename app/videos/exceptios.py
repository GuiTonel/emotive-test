from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR


class VideoProcessingError(APIException):
    status_code = HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _("Something happens to your request!")
    default_code = "video_processing_error"
