import io
import zipfile


def create_zip(dir_to_zip):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in dir_to_zip.iterdir():
            zip_file.write(file_path, arcname=file_path.name)
    return buffer
