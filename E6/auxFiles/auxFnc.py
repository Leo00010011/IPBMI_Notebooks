import numpy as np
import os
import sys
from PIL import Image
from math import floor

TISSUE_LABEL = {0: 'Adipose',
                1: 'Air',
                2: 'Bone',
                3: 'Breast',
                4: 'Soft',
                5: 'Water'}


def get_csv_data(tissue_index):
    csv_path = os.path.join(sys.path[0], 'auxFiles', 'coef',
                            'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
    if not os.path.exists(csv_path):
        csv_path = os.path.join(
            '.', 'auxFiles', 'coef', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')

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
        coef = np.interp(energy, [item[0]
                         for item in data], [item[1] for item in data])
    return coef

# for E6


def getCoef(fileName, eE):
    csv_path = os.path.join(sys.path[0], 'auxFiles', 'coef', fileName)
    if not os.path.exists(csv_path):
        csv_path = os.path.join('.', 'auxFiles', 'coef', fileName)

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
        coef = np.interp(eE, [item[0] for item in dataArr], [
                         item[1] for item in dataArr])
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


def getNumberPhotonsCell(qImage, N0):
    photon_distribution = np.zeros(len(qImage.flatten()), dtype=int)
    for photon_count in qImage.flatten():
        photon_distribution[int(photon_count)] += photon_count

    hist = [photon_distribution, qImage.flatten()]
    return hist


def insertArtifact(obj, pos, sizeArtifact, mu):
    radius = int(sizeArtifact / 2)
    x, y, z = pos
    x_range = range(x - radius, x + radius + 1)
    y_range = range(y - radius, y + radius + 1)
    z_range = range(z - radius, z + radius + 1)

    for i in x_range:
        for j in y_range:
            for k in z_range:
                distance = np.sqrt((i - x) ** 2 + (j - y) ** 2 + (k - z) ** 2)
                if distance < radius:
                    obj[k, j, i] = mu
    return obj


def down_scale_image(img, n, m):
    n0, m0 = img.shape
    cell_height = n0/n
    cell_width = m0/m
    row_rem = 1
    curr_row = 0
    value = 0
    result = np.zeros((n, m))
    for i in range(n):
        height_integer = floor(cell_height - row_rem)
        height_fraq = (cell_height - row_rem) - height_integer
        col_rem = 1
        curr_col = 0
        for j in range(m):

            width_integer = floor(cell_width - col_rem)
            width_fraq = (cell_width - col_rem) - width_integer

            # left up corner
            value += img[curr_row, curr_col]*row_rem*col_rem

            # upper row
            value += np.sum(img[curr_row, curr_col +
                            1: curr_col + width_integer + 1])*row_rem
            if width_fraq > 0.00000001:
                # right top corner
                value += img[curr_row, curr_col +
                             width_integer + 1]*row_rem*width_fraq

                # right column
                value += np.sum(img[curr_row + 1: curr_row + height_integer + 1,
                                    curr_col + width_integer + 1])*width_fraq

            if height_fraq > 0.00000001:
                # bottom row
                value += np.sum(img[curr_row + height_integer + 1,
                                    curr_col + 1: curr_col + width_integer + 1])*height_fraq

                # bottom left corner
                value += img[curr_row + height_integer +
                             1, curr_col]*height_fraq*col_rem

            if width_fraq > 0.00000001 and height_fraq > 0.00000001:
                # right bottom corner
                value += img[curr_row + height_integer + 1,
                             curr_col + width_integer + 1]*height_fraq*width_fraq

            # left column
            value += np.sum(img[curr_row + 1: curr_row + height_integer + 1,
                                curr_col])*col_rem

            # the middle
            value += np.sum(img[curr_row + 1: curr_row + height_integer + 1,
                                curr_col + 1: curr_col + width_integer + 1])
            result[i, j] = value
            value = 0
            curr_col += width_integer + 1
            col_rem = 1 - width_fraq

        curr_row += height_integer + 1
        row_rem = 1 - height_fraq

    return result


def detector_QDE(qImage: np.ndarray, n, m, qde):
    n0, m0 = qImage.shape
    if n == n0 and m == m0:
        return qImage
    
    result = None
    if n < n0 and m < m0:
        result = down_scale_image(qImage, n, m)

    elif n > n0 and m > m0:
        result = None
    else:
        raise NotImplementedError()
    result = result*qde
    return result


def detectorNoiseFullP_QDE(image, n, m, QDE):
    ideal = detector_QDE(image, n, m, QDE)
    noisy = np.random.poisson(ideal)
    return noisy


def getSNR(image, x0, y0, w):
    region = image[x0: x0 + w, y0: y0 + w]
    return np.mean(region)/np.std(region)
