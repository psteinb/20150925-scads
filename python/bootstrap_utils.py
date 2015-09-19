import random
from skimage.transform import rotate
import numpy as np

def random_rotate(_image, _seed = 0):
    """ rotates given image (aka numpy 3D array) by a random angle """
    random.seed(_seed)
    degrees = random.randrange(360)
    
    return rotate(_image,degrees)


def random_enhance_color(_image, _seed = 0, _color_id = -1):
    """ adds random value from [0,256) to random channel of _image, 
    if _color_id is -1, the channel is also chosen by a random number  """
    
    random.seed(_seed)
    if _color_id < 0 or _color_id > 2:
        _color_id = random.randrange(3)

    delta = random.randrange(0,255)

    value = np.copy(_image)
    cvals = value[...,_color_id]
    cvals[np.where(cvals < (256 - delta))] += delta
    value[...,_color_id] = cvals
    
    return value
