from django.http import FileResponse, HttpResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

from .serializers import ImageConvertSerializer, AudioConvertSerializer
from .utils.image import convert_image
from .utils.audio import convert_audio

PARSERS = [MultiPartParser, FormParser]


@api_view(['POST'])
@parser_classes(PARSERS)
def convert_image(request) -> FileResponse:
    serializer = ImageConvertSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    buf, mime = convert_image(
        serializer.validated_data['image'],
        serializer.validated_data['format']
    )

    return FileResponse(
        buf,
        content_type=mime,
        as_attachment=True,
        filename=f"converted.{serializer.validated_data['format'].lower()}",
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@parser_classes(PARSERS)
def convert_audio(request) -> HttpResponse:
    serializer = AudioConvertSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data, mime = convert_audio(
        serializer.validated_data['audio_file'],
        serializer.validated_data['format']
    )

    resp = HttpResponse(
        data,
        content_type=mime,
        status=status.HTTP_200_OK
    )
    resp['Content-Disposition'] = (
        f'attachment; filename="converted.'
        f'{serializer.validated_data["format"]}"'
    )
    return resp
