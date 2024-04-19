from typing import Iterable
import uuid
import hashlib
from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from videos.constants import RoverChoices, CameraChoices


class VideosModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.FileField(null=True, blank=True, upload_to="videos/")
    file_name = models.CharField(null=False, blank=False)
    requested_rover = models.CharField(
        max_length=3, choices=RoverChoices.choices, null=True, blank=True
    )
    requested_camera = models.CharField(
        max_length=7, choices=CameraChoices.choices, null=True, blank=True
    )
    requested_date = models.DateField(null=True, blank=True)
    is_done = models.BooleanField(null=False, blank=True, default=False)
    error = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "videos_request"
        verbose_name = _("Mars Videos Request")

    @property
    def has_error(self):
        return True if self.error else False

    def save(self, *args, **kwargs) -> None:
        if not self.file_name:
            file_name = (
                self.requested_rover if self.requested_rover else RoverChoices.CURIOSITY
            )
            file_name += (
                self.requested_camera if self.requested_camera else CameraChoices.FHAZ
            )
            file_name += (
                self.requested_date.strftime("%Y-%m-%d")
                if self.requested_date
                else datetime.now().date().strftime("%Y-%m-%d")
            )
            self.file_name = hashlib.md5(file_name.encode()).hexdigest() + ".gif"

        return super(VideosModel, self).save(*args, **kwargs)
