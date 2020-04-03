import os.path
from hashlib import sha3_256
from functools import reduce
from typing import List, Type, Tuple

from transform.models import TransformationChain
from transform.transformations import Transformation, TransformationParameters
from image.models import Image

from PIL import Image as PILImage
from django.utils.functional import cached_property
from django.conf import settings


class TransformationChainExecutor:
    def __init__(self, image: Image, chain: List[Tuple[Type[Transformation], Type[TransformationParameters]]]):
        self._tuple = (str(image.pk), tuple(map(lambda tpl: (tpl[0].__name__.lower(), tpl[1]), chain)))

        self.image = image
        self.chain = chain

    def __hash__(self):
        return hash(self._tuple)

    @cached_property
    def sha256(self):
        return sha3_256(
            hash(self).to_bytes(
                settings.GLAZE['HASH_BYTE_ARRAY_LENGTH'],
                byteorder='big',
                signed=True,
            )
        ).hexdigest()

    def execute(self) -> TransformationChain:
        image_file = PILImage.open(self.image.file)
        source_image = image_file.copy()
        source_image.format = image_file.format
        image_file.close()

        transformed_image = reduce(lambda img, tpl: tpl[0].transform(img, tpl[1]), self.chain, source_image)

        destination_path = os.path.join(
            settings.MEDIA_ROOT,
            TransformationChain.file.field.upload_to,
            self.sha256 + '.' + transformed_image.format.lower(),
        )

        transformed_image.save(destination_path)

        return TransformationChain.objects.create(
            id=self.sha256,
            image=self.image,
            file=destination_path,
            extension=transformed_image.format.lower(),
            mime=PILImage.MIME[transformed_image.format],
        )
