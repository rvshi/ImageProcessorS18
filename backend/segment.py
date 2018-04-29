# import matplotlib.pyplot as plt
from skimage import filters
from skimage import exposure
from convert import convert_image
import scipy.ndimage as ndimage
from convert import get_image_by_uuid, save_image_from_arr


def segment(uuid):
    uintfile = get_image_by_uuid(uuid)
    val = filters.threshold_otsu(uintfile)
    hist, bins_center = exposure.histogram(uintfile)
    binary_img = uintfile < val
    open_img = ndimage.binary_opening(binary_img)  # remove small white regions
    close_img = ndimage.binary_closing(open_img)  # remove small black regions
    new_uuid = save_image_from_arr(close_img)
    return new_uuid
