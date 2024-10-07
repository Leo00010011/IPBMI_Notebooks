import os
import sys
import numpy as np

TISSUE_LABEL = {0: 'Adipose',
                1: 'Air',
                2: 'Bone',
                3: 'Breast',
                4: 'Soft',
                5: 'Water'}


def get_csv_data(tissue_index, csv_path=None):
    if not csv_path:
        csv_path = os.path.join(
            sys.path[0], 'auxFiles', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
    else:
        csv_path = os.path.join(
            csv_path, 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
    dataArr = []
    with open(csv_path, 'r') as file:
        next(file)
        next(file)
        for line in file:
            line = line.strip().split('\t')
            listFromLine = [float(item) for item in line]
            dataArr.append(listFromLine)
    return dataArr


def get_coef(index, energy, csv_path=None):
    data = get_csv_data(index, csv_path)
    coef = 0
    for item in data:
        if item[0] == energy:
            coef = item[1]
            break
    return coef


def normalize_data(data):
    return np.round(data/data.max(), 2) * 256


def getLine(data, nLine):
    lines = data[:, nLine]
    return lines
