from typing import List, Type, Tuple

from image.models import Image
from transform.transformations import (
    Transformation,
    TransformationParameters,
    TRANSFORMATIONS,
    TRANSFORMATION_PARAMETERS_PATTERNS,
)


class StringParser:
    def __init__(self, image: Image, transformation_delimeter: str = '|', parameters_delimeter: str = '='):
        self.image = image
        self.transformation_delimeter = transformation_delimeter
        self.parameters_delimeter = parameters_delimeter

    def parse_params(self, param_string: str) -> TransformationParameters:
        for pattern in TRANSFORMATION_PARAMETERS_PATTERNS:
            match = pattern.fullmatch(param_string)

            if match is not None:
                return TRANSFORMATION_PARAMETERS_PATTERNS[pattern](**match.groupdict())

        raise ValueError('Invalid parameters string')

    def parse(self, chain_string: str) -> List[Tuple[Type[Transformation], Type[TransformationParameters]]]:
        chain = chain_string.strip(self.transformation_delimeter).split(self.transformation_delimeter)

        parsed_chain = []

        for chain_part in chain:
            transformation_string, params_string = chain_part.split(self.parameters_delimeter)

            if transformation_string not in TRANSFORMATIONS:
                raise ValueError('Unsupported transformation type')

            transformation = TRANSFORMATIONS[transformation_string]
            params = self.parse_params(params_string)

            parsed_chain.append((transformation, params))

        return parsed_chain
