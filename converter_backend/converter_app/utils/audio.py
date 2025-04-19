import os, tempfile
from pydub import AudioSegment


def convert_audio(uploaded_file, target_format) -> tuple[bytes, str]:
    with tempfile.NamedTemporaryFile(delete=False) as inp:
        for chunk in uploaded_file.chunks():
            inp.write(chunk)
        inp_path = inp.name

    try:
        aud = AudioSegment.from_file(inp_path)
        with tempfile.NamedTemporaryFile(suffix=f".{target_format}", delete=False) as outp:
            aud.export(outp.name, format=target_format)
            outp_path = outp.name

        with open(outp_path, "rb") as f:
            data = f.read()
    finally:
        os.remove(inp_path)
        if os.path.exists(outp_path):
            os.remove(outp_path)

    return data, f"audio/{target_format}"
