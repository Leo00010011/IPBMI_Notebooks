import numpy as np
import os, sys

TISSUE_LABEL = {0: 'Adipose',
                1: 'Air',
                2: 'Bone',
                3: 'Breast',
                4: 'Soft',
                5: 'Water'}


def get_csv_data(tissue_index):
    csv_path = os.path.join(sys.path[0], 'auxFiles', 'coef', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join('.','auxFiles' ,'coef', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
    dataArr = []
    with open(csv_path, 'r') as file:
        next(file)
        next(file)
        for line in file:
            line = line.strip().split('\t')
            listFromLine = [float(item) for item in line]
            dataArr.append(listFromLine)
    return dataArr

def get_coef(index, energy):
    data = get_csv_data(index)
    coef = 0
    for item in data:
        if item[0] == energy:
            coef = item[1]
            break
    if coef == 0:
        coef = np.interp(energy,[item[0] for item in data], [item[1] for item in data])
    return coef

# for E6
def getCoef(fileName, eE):
    csv_path = os.path.join(sys.path[0], 'auxFiles', 'coef', fileName)
    dataArr = []
    with open(csv_path, 'r') as file:
        next(file)
        next(file)
        for line in file:
            line = line.strip().split('\t')
            if line == ['']:
                continue
            listFromLine = [float(item) for item in line]
            dataArr.append(listFromLine)
                
    coef = 0
    for item in dataArr:
        if item[0] == eE:
            coef = float(item[1])
            break
    if coef == 0:
        coef = np.interp(eE,[item[0] for item in dataArr], [item[1] for item in dataArr])
    return coef

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

def getNumberCellsPhoton(qImage, N0):
    photon_distribution = np.zeros(N0 + 1, dtype=int)
    for photon_count in qImage.flatten():
        if photon_count <= N0:
            photon_distribution[int(photon_count)] += 1
    
    hist = [photon_distribution, photon_distribution.flatten()]
    return hist