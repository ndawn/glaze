from rest_framework import status
from rest_framework.exceptions import APIException


class NoFileProvided(APIException):
    default_detail = 'No file provided'
    default_code = 'no_file_provided'
    status_code = status.HTTP_400_BAD_REQUEST


class NoURLProvided(APIException):
    default_detail = 'No URL provided'
    default_code = 'no_url_provided'
    status_code = status.HTTP_400_BAD_REQUEST


class MaxFileSizeExceeded(APIException):
    default_detail = 'File size exceeds the limit'
    default_code = 'max_file_size_exceeded'
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedFileType(APIException):
    default_detail = 'Unsupported file type'
    default_code = 'unsupported_file_type'
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
