from PIL import Image
from glaze.types import PilImage


class Transformation:
    def __init__(self, image):
        if isinstance(image, PilImage):
            self.image = image
        elif isinstance(image, str):
            self.image = Image.open(image)
        else:
            raise TypeError('\'image\' argument must be either a PIL image object or a string containing file path')

    def transform(self):
        pass


class Crop(Transformation):
    def transform(self):
        pass
