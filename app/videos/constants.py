from enum import unique
from django.db.models import TextChoices


@unique
class RoverChoices(TextChoices):
    CURIOSITY = "CUR", "curiosity"
    OPPORTUNITY = "OPP", "opportunity"
    SPIRIT = "SPI", "spirit"


@unique
class CameraChoices(TextChoices):
    FHAZ = "FHAZ", "Front Hazard Avoidance Camera"
    RHAZ = "RHAZ", "Rear Hazard Avoidance Camera"
    MAST = "MAST", "Mast Camera"
    CHEMCAM = "CHEMCAM", "Chemistry and Camera Complex"
    MAHLI = "MAHLI", "Mars Hand Lens Imager"
    MARDI = "MARDI", "Mars Descent Imager"
    NAVCAM = "NAVCAM", "Navigation Camera"
    PANCAM = "PANCAM", "Panoramic Camera"
    MINITES = "MINITES", "Miniature Thermal Emission Spectrometer (Mini-TES)"
