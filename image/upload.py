import os
from uuid import UUID

from accounts.models import User
from image.filetypes import check_file_type
from image.models import Image


class UploadedImageProcessor:
    @staticmethod
    def create(file_uuid: UUID, file_path: str, file_name: str, file_owner: User):
        file_extension, file_mime = check_file_type(file_path)

        file_path_with_extension = file_path + '.' + file_extension

        os.rename(file_path, file_path_with_extension)

        return Image.objects.create(
            id=file_uuid,
            name=file_name,
            extension=file_extension,
            mime=file_mime,
            owner=file_owner,
            file=file_path_with_extension,
        )
