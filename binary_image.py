
import numpy as np
from PIL import Image
import cython


def binary_image(path,save=True,th=128):
    """
     Binarizacion of an image
    Parameters
    ----------
   path : str
         path directory
    save : boolean
         save image default "output.png"
    th : int
        thresholding
    """
    im = np.array(Image.open(path).convert('L').resize((256, 256)))
    im_bin_th = (im > th) * 255
    if(save):
        Image.fromarray(np.uint8(im_bin_th)).save("output.png")
    return im_bin_th

