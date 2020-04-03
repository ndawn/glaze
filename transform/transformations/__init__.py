import os
import re
from typing import Type
from time import time

from .parameters import (
    TransformationParameters,
    SingleIntParameter,
    SingleFloatParameter,
    SingleStringParameter,
    IntXYParameters,
    IntXYWHParameters,
)

from django.conf import settings
from PIL.ImageFilter import GaussianBlur
from PIL.Image import Image as PILImageClass
from PIL import Image


class Transformation:
    @staticmethod
    def transform_with_single_int(image: PILImageClass, params: SingleIntParameter) -> PILImageClass:
        raise NotImplementedError()

    @staticmethod
    def transform_with_single_float(image: PILImageClass, params: SingleFloatParameter) -> PILImageClass:
        raise NotImplementedError()

    @staticmethod
    def transform_with_single_string(image: PILImageClass, params: SingleStringParameter) -> PILImageClass:
        raise NotImplementedError()

    @staticmethod
    def transform_with_int_x_y(image: PILImageClass, params: IntXYParameters) -> PILImageClass:
        raise NotImplementedError()

    @staticmethod
    def transform_with_int_x_y_w_h(image: PILImageClass, params: IntXYWHParameters) -> PILImageClass:
        raise NotImplementedError()

    @classmethod
    def transform(cls, image: PILImageClass, params: Type[TransformationParameters]) -> PILImageClass:
        if isinstance(params, SingleIntParameter):
            return cls.transform_with_single_int(image, params)
        elif isinstance(params, SingleFloatParameter):
            return cls.transform_with_single_float(image, params)
        elif isinstance(params, SingleStringParameter):
            return cls.transform_with_single_string(image, params)
        elif isinstance(params, IntXYParameters):
            return cls.transform_with_int_x_y(image, params)
        elif isinstance(params, IntXYWHParameters):
            return cls.transform_with_int_x_y_w_h(image, params)

        raise ValueError('Invalid parameter set')


class Crop(Transformation):
    @staticmethod
    def transform_with_single_int(image: PILImageClass, params: SingleIntParameter) -> PILImageClass:
        half_width = image.width // 2
        half_height = image.height // 2
        half_parameter = params.int_value // 2

        transformed_image = image.crop((
            half_width - half_parameter,
            half_height - half_parameter,
            half_width + half_parameter,
            half_height + half_parameter,
        ))

        transformed_image.format = image.format

        return transformed_image

    @staticmethod
    def transform_with_int_x_y(image: PILImageClass, params: IntXYParameters) -> PILImageClass:
        half_width = image.width // 2
        half_height = image.height // 2
        half_x = params.x // 2
        half_y = params.y // 2

        transformed_image = image.crop((
            half_width - half_x,
            half_height - half_y,
            half_width + half_x,
            half_height + half_y,
        ))

        transformed_image.format = image.format

        return transformed_image

    @staticmethod
    def transform_with_int_x_y_w_h(image: PILImageClass, params: IntXYWHParameters) -> PILImageClass:
        transformed_image = image.crop((
            params.x,
            params.y,
            params.w,
            params.h,
        ))

        transformed_image.format = image.format

        return transformed_image


class Resize(Transformation):
    @staticmethod
    def transform_with_single_int(image: PILImageClass, params: SingleIntParameter) -> PILImageClass:
        transformed_image = image.resize((
            params.int_value,
            params.int_value,
        ))

        transformed_image.format = image.format

        return transformed_image

    @staticmethod
    def transform_with_int_x_y(image: PILImageClass, params: IntXYParameters) -> PILImageClass:
        transformed_image = image.resize((
            params.x,
            params.y,
        ))

        transformed_image.format = image.format

        return transformed_image


class Rotate(Transformation):
    @staticmethod
    def transform_with_single_int(image: PILImageClass, params: SingleIntParameter) -> PILImageClass:
        transformed_image = image.rotate(params.int_value)
        transformed_image.format = image.format
        return transformed_image


class Blur(Transformation):
    @staticmethod
    def transform_with_single_int(image: PILImageClass, params: SingleIntParameter) -> PILImageClass:
        transformed_image = image.filter(GaussianBlur(params.int_value))
        transformed_image.format = image.format
        return transformed_image

    @staticmethod
    def transform_with_single_float(image: PILImageClass, params: SingleFloatParameter) -> PILImageClass:
        transformed_image = image.filter(GaussianBlur(params.float_value))
        transformed_image.format = image.format
        return transformed_image


class Format(Transformation):
    @staticmethod
    def transform_with_single_string(image: PILImageClass, params: SingleStringParameter) -> PILImageClass:
        fmt = params.str_value.upper()

        if fmt not in Image.MIME:
            raise ValueError('Unsupported image format')

        temp_path = os.path.join(
            settings.GLAZE['TEMP_DIRECTORY'],
            str(time()) + params.str_value,
        )

        image.save(temp_path, params.str_value)

        temp_image = Image.open(temp_path)
        transformed_image = temp_image.copy()
        transformed_image.format = temp_image.format
        temp_image.close()
        os.remove(temp_path)

        return transformed_image


TRANSFORMATIONS = {
    'crop': Crop,
    'resize': Resize,
    'rotate': Rotate,
    'blur': Blur,
    'format': Format,
}

TRANSFORMATION_PARAMETERS_PATTERNS = {
    re.compile(r'^(?P<int_value>-?\d+)$'): SingleIntParameter,
    re.compile(r'^(?P<float_value>-?\d+\.\d+)$'): SingleFloatParameter,
    re.compile(r'^(?P<x>-?\d+)x(?P<y>-?\d+)$'): IntXYParameters,
    re.compile(r'^(?P<w>-?\d+)x(?P<h>-?\d+):(?P<x>-?\d+),(?P<y>-?\d+)$'): IntXYWHParameters,
    re.compile(r'^(?P<str_value>.+)$'): SingleStringParameter,
}
