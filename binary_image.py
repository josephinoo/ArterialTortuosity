from scipy.misc import imread, imsave



def binaryImage(path,saveImage=False):
    img = imread(path, mode='L')
    threshold = 150
    binarized = 1.0 * (img > threshold)
    if(saveImage):
        imsave('binarized.jpg', binarized)
    return binarized

    