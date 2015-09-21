import random
from skimage.transform import rotate
import numpy as np
from skimage import io
import os
import time

def random_rotate(_image, _seed = 0, _verbose=False):
    """ rotates given image (aka numpy 3D array) by a random angle """

    random.seed(_seed)
    if not _seed:
        random.seed(time.time())
        
    degrees = random.randrange(360)
    if _verbose:
        print __file__," rotating by ",degrees
        
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

def change_and_write(_fname,_image,_args):

    value = _image
    if not _args.color_only:    
        value = random_rotate(value,0,_args.verbose)
        
    if not _args.rotate_only:    
        value = random_enhance_color(value)

    #write to disk
    namebase,nameext = os.path.splitext(_fname)
    name2save = namebase+_args.name_insert+nameext
    io.imsave(name2save,value)
    
    if _args.verbose:
        print name2save, " written to disk"

def wrap_change_and_write(_tuple):
    change_and_write(_tuple[0], _tuple[1], _tuple[2])
