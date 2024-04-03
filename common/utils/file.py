from server.settings import MEDIA_ROOT


def file_field_path_delete(field_name, request_data, file_field):
    if field_name in request_data and file_field:
        file_path = MEDIA_ROOT / str(file_field)
        if file_path.exists():
            file_path.unlink()
