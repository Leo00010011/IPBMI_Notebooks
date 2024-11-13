import numpy as np
try:
    from auxFiles.auxFnc import *
except:
    from auxFnc import *

def setHounsfield(Image, eE):
    water_coef = get_coef(5,eE)
    return ((Image - water_coef)/water_coef)*1000

def displayWL(Image, W, L, maxGL):
    min_intensity = L - W/2
    Image = (Image - min_intensity)/W
    Image[Image < 0] = 0
    Image[Image > 1] = 1
    Image = Image*maxGL
    return Image
