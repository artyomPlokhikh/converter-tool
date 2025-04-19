from rest_framework import serializers


class ImageConvertSerializer(serializers.Serializer):
    image = serializers.ImageField()
    format = serializers.ChoiceField(choices=[
        ("JPEG", "JPEG"), ("BMP", "BMP"),
        ("GIF", "GIF"), ("PNG", "PNG"),
        ("ICO", "ICO"),
    ])


class AudioConvertSerializer(serializers.Serializer):
    audio_file = serializers.FileField()
    format = serializers.ChoiceField(choices=[
        ("wav", "WAV"), ("mp3", "MP3"),
        ("ogg", "OGG"), ("flac", "FLAC"),
    ])
