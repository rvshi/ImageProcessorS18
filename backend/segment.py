# import matplotlib.pyplot as plt
from skimage import filters
from skimage import exposure
from convert import convert_image
import scipy.ndimage as ndimage


def segment(img_str):
    uintfile = convert_image(img_str)
    val = filters.threshold_otsu(uintfile)
    hist, bins_center = exposure.histogram(uintfile)
    binary_img = uintfile < val
    open_img = ndimage.binary_opening(binary_img)  # remove small white regions
    close_img = ndimage.binary_closing(open_img)  # remove small black regions

    # plotting

    # plt.figure(figsize=(9, 4))
    # plt.subplot(231)
    # plt.imshow(uintfile, cmap='gray', interpolation='nearest')
    # plt.axis('off')
    # plt.subplot(232)
    # # plt.imshow(otsu_img, cmap='gray', interpolation='nearest')
    # # plt.axis('off')
    # plt.subplot(233)
    # plt.plot(bins_center, hist, lw=2)
    # plt.axvline(val, color='k', ls='--')
    # plt.subplot(234)
    # plt.imshow(open_img, cmap='gray', interpolation='nearest')
    # plt.axis('off')
    # plt.subplot(235)
    # plt.imshow(close_img, cmap='gray', interpolation='nearest')
    # plt.axis('off')

    # plt.tight_layout()
    # plt.show()
