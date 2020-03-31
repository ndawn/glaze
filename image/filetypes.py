from typing import Union, Tuple
from abc import ABC, abstractmethod

from django.conf import settings


class FileTypeChecker(ABC):
    extension = None
    mime = None

    @classmethod
    def get_file_type(cls):
        return cls.extension, cls.mime

    @staticmethod
    @abstractmethod
    def check(file_path: str):
        pass


class JpegFileTypeChecker(FileTypeChecker):
    extension = 'jpeg'
    mime = 'image/jpeg'

    magic_bytes = [
        bytearray([0xff, 0xd8, 0xff, 0xdb]),
        bytearray([0xff, 0xd8, 0xff, 0xe0]),
        bytearray([0xff, 0xd8, 0xff, 0xe1]),
    ]

    @staticmethod
    def check(first_bytes: Union[bytes, bytearray]):
        for byte_sequence in JpegFileTypeChecker.magic_bytes:
            if first_bytes.startswith(byte_sequence):
                return True

        return False


class PngFileTypeChecker(FileTypeChecker):
    extension = 'png'
    mime = 'image/png'

    magic_bytes = [
        bytearray([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    ]

    @staticmethod
    def check(first_bytes: Union[bytes, bytearray]):
        for byte_sequence in PngFileTypeChecker.magic_bytes:
            if first_bytes.startswith(byte_sequence):
                return True

        return False


class TiffFileTypeChecker(FileTypeChecker):
    extension = 'tiff'
    mime = 'image/tiff'

    magic_bytes = [
        bytearray([0x49, 0x49, 0x2a, 0x00]),
        bytearray([0x4d, 0x4d, 0x00, 0x2a]),
    ]

    @staticmethod
    def check(first_bytes: Union[bytes, bytearray]):
        for byte_sequence in TiffFileTypeChecker.magic_bytes:
            if first_bytes.startswith(byte_sequence):
                return True

        return False


class WebpFileTypeChecker(FileTypeChecker):
    extension = 'webp'
    mime = 'image/webp'

    magic_bytes = [
        bytearray([0x52, 0x49, 0x46, 0x46, 0x00, 0x00, 0x00, 0x00, 0x57, 0x45, 0x42, 0x50]),
    ]

    @staticmethod
    def check(first_bytes: Union[bytes, bytearray]):
        return (first_bytes[:4] == WebpFileTypeChecker.magic_bytes[0][:4]) \
               and (first_bytes[8:12] == WebpFileTypeChecker.magic_bytes[0][8:12])


FILETYPE_CHECKERS = [JpegFileTypeChecker, PngFileTypeChecker, TiffFileTypeChecker, WebpFileTypeChecker]


def check_file_type(file_path: str) -> Tuple[str, str]:
    with open(file_path, 'rb') as file:
        detection_byte_sequence = file.read(settings.FILETYPE_DETECTION_BYTE_SEQUENCE_LENGTH)

    for checker in FILETYPE_CHECKERS:
        if checker.check(detection_byte_sequence):
            return checker.get_file_type()

    raise ValueError('Unsupported file type')
