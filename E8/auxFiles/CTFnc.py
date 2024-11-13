import numpy as np
try:
    from auxFiles.auxFnc import *
except:
    from auxFnc import *

def setHounsfield(Image, eE):
    water_coef = get_coef(5,eE)
    return (Image - water_coef)/water_coef*1000

def displayWL(Image, W, L, maxGL):
    min_intensity = L - W/2
    Image -= min_intensity
    Image = np.clip(Image, 0, W)
    return Image/W*maxGL
