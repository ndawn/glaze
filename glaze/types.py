from PIL.BmpImagePlugin import BmpImageFile
from PIL.JpegImagePlugin import JpegImageFile
from PIL.PngImagePlugin import PngImageFile
from PIL.TiffImagePlugin import TiffImageFile
from PIL.WebPImagePlugin import WebPImageFile


from typing import Union


PilImage = Union[BmpImageFile, JpegImageFile, PngImageFile, TiffImageFile, WebPImageFile]
