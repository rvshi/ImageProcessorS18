"""Module to handle segmentation process.

"""
from numpy import uint8
from skimage import filters
from skimage import exposure
import scipy.ndimage as ndimage
from images import get_image_by_uuid, save_image_from_arr
import logging
from logging_config import config


logging.basicConfig(**config)
logger = logging.getLogger(__name__)


def segment(uuid):
    """Segments image with input uuid, saves processed image to server
    and returns its uuid

       :param uuid: uuid of original image
       :returns: uuid of processed image, saves b64 string of image on server
    """
    logger.info('Retrieve current image and perform segmentation')
    uintfile = get_image_by_uuid(uuid)

    logger.debug('Original image UUID: {}'.format(uuid))
    val = filters.threshold_otsu(uintfile)
    hist, bins_center = exposure.histogram(uintfile)
    binary_img = uintfile >= val
    open_img = ndimage.binary_opening(binary_img)
    close_img = ndimage.binary_closing(open_img)
    new_image = uint8(close_img * 255)
    new_uuid = save_image_from_arr(new_image)
    logger.debug('Segmentation complete. New image UUID: {}'.format(new_uuid))
    return new_uuid
