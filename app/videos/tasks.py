import os
import traceback
from datetime import datetime
from PIL import Image
from io import BytesIO

import requests
from django.conf import settings
from celery import shared_task

from videos.models import VideosModel
from videos.constants import RoverChoices, CameraChoices


@shared_task()
def process_video(
    id, file_name=None, requested_rover=None, requested_camera=None, requested_date=None
):
    instance = VideosModel.objects.get(pk=id)
    try:
        if not file_name:
            raise Exception("File name not informed!")
        file_path = os.path.join(settings.MEDIA_ROOT, "videos", file_name)
        if os.path.exists(file_path):
            instance.file.name = "./videos/" + file_name
            instance.is_done = True
            instance.save(update_fields=["file", "is_done"])
            return

        url = settings.NASA_ROVER_URL % (
            instance.get_requested_rover_display()
            if requested_rover
            else RoverChoices.choices[0][1]
        )
        params = {"api_key": settings.NASA_API_KEY, "camera": requested_camera}

        if not requested_camera:
            params["camera"] = CameraChoices.FHAZ

        if requested_date:
            params["earth_date"] = requested_date.strftime("%Y-%m-%d")
        else:
            params["earth_date"] = datetime.now().date().strftime("%Y-%m-%d")

        res = requests.get(url, params=params)
        if not res.ok:
            params.pop("api_key")
            raise Exception(f"Request not succed: params: {params} | URL: {url}")

        content = res.json()

        frames = []
        if content["photos"]:
            for photo in content["photos"]:
                frame = Image.open(
                    BytesIO(requests.get(photo["img_src"], stream=True).content)
                )
                frames.insert(0, frame)

            frames[0].save(file_path, save_all=True, append_images=frames[1:])

            instance.file.name = "./videos/" + file_name
            instance.is_done = True
            instance.save(update_fields=["file", "is_done"])
        else:
            instance.file.name = "./videos/empty.gif"
            instance.is_done = True
            instance.save(update_fields=["file", "is_done"])

    except Exception:
        instance.error = traceback.format_exc()
        instance.save(update_fields=["error"])
