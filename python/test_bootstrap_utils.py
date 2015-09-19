from skimage import data
from bootstrap_utils import random_rotate, random_enhance_color

def test_random_rotate():
    image = data.coins() 
    rotated = random_rotate(image,_seed=42)
    assert (image != rotated).all()
    assert (image.shape == rotated.shape)
    assert (image.sum() > rotated.sum())
    
def test_random_enhance_color():
    image = data.coffee()
    enhanced = random_enhance_color(image,_seed=42, _color_id=0)
    assert (image[...,0] != enhanced[...,0]).any()
    assert (image.shape == enhanced.shape)
    assert (image.sum() < enhanced.sum())

def test_random_enhance_any_color():
    image = data.coffee()

    for i in xrange(10):
        enhanced = random_enhance_color(image,_seed=42)
        assert (image != enhanced).any()
        assert (image.shape == enhanced.shape)
        assert (image.sum() < enhanced.sum())


