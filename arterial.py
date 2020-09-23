

import numpy as np
from PIL import Image

class Arterial:
    def __init__(self,path):
        self.__path=path
    
    def generateArterial(self):
        return 0
    
    def convert3D(self):
        return None


    def networkArterial(self):
        return None
    
    def binary_image(selfsave=True,th=128):
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
    im = np.array(Image.open(self.__path).convert('L').resize((256, 256)))
    im_bin_th = (im > th) * 255
    if(save):
        Image.fromarray(np.uint8(im_bin_th)).save("output.png")
    return im_bin_th
