import numpy as np
from auxFiles.auxFnc import get_coef
import matplotlib.pyplot as plt

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE

def cube_phantom_nh(edge_size, energy):
    soft_coef = round(get_coef(4, energy), 2)
    air_coef = round(get_coef(1, energy), 2)
    water_coef = round(get_coef(5, energy), 2)
    print(soft_coef, air_coef, water_coef)
    if edge_size > 2 and np.log2(edge_size) % 1 == 0:
        tissue_edge = int(edge_size / 2)
        offset = int((edge_size - tissue_edge) / 2)
        phantom = np.zeros((edge_size, edge_size, edge_size))
        phantom[:, :, :] = air_coef
        phantom[:, :, tissue_edge:] = water_coef
        phantom[offset:offset + tissue_edge, offset: offset +
                tissue_edge, offset:offset+tissue_edge] = soft_coef
        return phantom
    else:
        print('not powers of 2')
        return
    
def interactor_PR(N0, obj, prj):
    coef_sum = 0.0
    if prj == 'frontal':
        coef_sum = np.sum(obj, axis=2)
    elif prj == 'lateral':
        coef_sum = np.sum(obj, axis=0)
    else:
        print('please input the right parameter: frontal or lateral')
        return False
    return N0 * np.exp((-coef_sum / coef_sum.shape[0]))

def getNumberPhotons(qImage):
    photons_num = np.sum(qImage)
    return int(photons_num)

def getNumberPhotonsCell(qImage, N0):
    photon_distribution = np.zeros(N0 + 1, dtype=int)
    for photon_count in qImage.flatten():
        if photon_count <= N0:
            photon_distribution[int(photon_count)] += photon_count
    
    hist = [photon_distribution, qImage.flatten()]
    return hist

def getNumberCellsPhoton(qImage, N0):
    photon_distribution = np.zeros(N0 + 1, dtype=int)
    for photon_count in qImage.flatten():
        if photon_count <= N0:
            photon_distribution[int(photon_count)] += 1
    
    hist = [photon_distribution, photon_distribution.flatten()]
    return hist


def detectorNoiseP_1_1(qImage):
    Poisson = np.random.poisson(qImage)
    dImgNum = getNumberPhotons(Poisson)
    imgNum = getNumberPhotons(qImage)
    if dImgNum >= imgNum:
        return detectorNoiseP_1_1(qImage)
    else:
        print('N Cells:',  Poisson.shape[0], Poisson.shape[1])
        return Poisson