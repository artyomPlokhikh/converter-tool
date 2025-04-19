from django.urls import path, include, re_path
from rest_framework.decorators import api_view
from django.views.generic import RedirectView
from rest_framework.response import Response


@api_view(['GET'])
def api_index(request):
    return Response({
        "convert_image": request.build_absolute_uri("/api/convert-image"),
        "convert_audio": request.build_absolute_uri("/api/convert-audio"),
    })


urlpatterns = [
    path("", api_index, name="api-index"),

    path("api/", include("converter_app.urls", namespace="converter")),
    re_path(r"^.*$", RedirectView.as_view(pattern_name="api-index", permanent=False)),
]
