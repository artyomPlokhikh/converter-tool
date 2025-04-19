from PIL import Image
from io import BytesIO


def convert_image(image_file, target_format) -> tuple[BytesIO, str]:
    img = Image.open(image_file)
    if target_format.upper() == "JPEG":
        img = img.convert("RGB")
    if target_format.upper() == "ICO":
        img = img.resize((50, 50))
    buf = BytesIO()
    save_kwargs = {"sizes": [(50, 50)]} if target_format.upper() == "ICO" else {}
    img.save(buf, format=target_format, **save_kwargs)
    buf.seek(0)
    mime = {
        "JPEG": "image/jpeg", "BMP": "image/bmp",
        "GIF": "image/gif", "PNG": "image/png",
        "ICO": "image/x-icon",
    }.get(target_format.upper(), "application/octet-stream")
    return buf, mime
