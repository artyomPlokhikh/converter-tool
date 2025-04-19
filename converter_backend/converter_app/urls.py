from .api import convert_image, convert_audio
from django.urls import path

app_name = "converter_app"

urlpatterns = [
    path("convert-image", convert_image, name="convert-image"),
    path("convert-audio", convert_audio, name="convert-audio"),
]
