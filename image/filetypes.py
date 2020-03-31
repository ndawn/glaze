from typing import Union, Tuple

from django.conf import settings


def detect_file_type(file_path: str) -> Union[Tuple[str, str], Tuple[None, None]]:
    with open(file_path, 'rb') as file:
        first_bytes = file.read(settings.FILETYPE_DETECTION_BYTES_READ_COUNT)

    for extension in FILETYPES.keys():
        if extension in CUSTOM_DETECTION_ALGORITHM:
            if CUSTOM_DETECTION_ALGORITHM[extension](first_bytes):
                return extension, FILETYPES[extension]['mime']
        else:
            for magic_bytes in FILETYPES[extension]['magic_bytes']:
                if first_bytes.startswith(magic_bytes):
                    return extension, FILETYPES[extension]['mime']

    return None, None


def is_webp(first_bytes: Union[bytes, bytearray]) -> bool:
    if (first_bytes[:4] == FILETYPES['webp']['magic_bytes'][0][:4]) \
            and (first_bytes[8:12] == FILETYPES['webp']['magic_bytes'][0][8:12]):
        return True


CUSTOM_DETECTION_ALGORITHM = {
    'webp': is_webp,
}


FILETYPES = {
    'jpeg': {
        'mime': 'image/jpeg',
        'magic_bytes': [
            bytearray([0xff, 0xd8, 0xff, 0xdb]),
            bytearray([0xff, 0xd8, 0xff, 0xe0]),
            bytearray([0xff, 0xd8, 0xff, 0xe1]),
        ],
    },
    'png': {
        'mime': 'image/png',
        'magic_bytes': [
            bytearray([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
        ],
    },
    'tiff': {
        'mime': 'image/tiff',
        'magic_bytes': [
            bytearray([0x49, 0x49, 0x2a, 0x00]),
            bytearray([0x4d, 0x4d, 0x00, 0x2a]),
        ],
    },
    'webp': {
        'mime': 'image/webp',
        'magic_bytes': [
            bytearray([0x52, 0x49, 0x46, 0x46, 0x00, 0x00, 0x00, 0x00, 0x57, 0x45, 0x42, 0x50]),
        ]
    },
}
