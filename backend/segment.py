from numpy import uint8
from skimage import filters
from skimage import exposure
import scipy.ndimage as ndimage
from images import get_image_by_uuid, save_image_from_arr


def segment(uuid):
    """Segments image with input uuid, saves processed image to server
    and returns its uuid

       :param uuid: uuid of original image
       :returns: uuid of processed image, saves b64 string of image on server
    """
    uintfile = get_image_by_uuid(uuid)
    val = filters.threshold_otsu(uintfile)
    hist, bins_center = exposure.histogram(uintfile)
    binary_img = uintfile >= val
    struct = ndimage.morphology.generate_binary_structure(3, 3)
    open_img = ndimage.binary_opening(binary_img, struct)
    close_img = ndimage.binary_closing(open_img, struct)
    new_image = uint8(close_img * 255)
    new_uuid = save_image_from_arr(new_image)
    return new_uuid
