
import numpy as np

from PIL import Image

import cython


def binary_image(path,save=True,th=128):
    """
    Binarizacion de un imagen , a parti de un path 
    @return imagen binarizadad
    """
    im = np.array(Image.open(path).convert('L').resize((256, 256)))
    im_bin_th = (im > th) * 255
    if(save):
        Image.fromarray(np.uint8(im_bin_th)).save("output.png")
    return im_bin_th

