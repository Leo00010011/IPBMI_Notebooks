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
        csv_path = os.path.join('.', 'auxFiles', 'coef', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
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
            print(item[0])
            print(item[1])
            coef = item[1]
            break
    if coef == 0:
        coef = np.interp(energy,[item[0] for item in data], [item[1] for item in data])
    return coef

def getContrast(image, x0, y0, x1, y1, w):
    region_a = np.mean(image[x0: x0 + w, y0: y0 + w])
    region_b = np.mean(image[x1: x1 + w, y1: y1 + w])
    max_i = np.max(image)
    return np.abs(region_a - region_b)/max_i    

def getSNR(image, x0, y0, w):
    region = image[x0: x0 + w,y0: y0 + w]
    return np.mean(region)/np.std(region)