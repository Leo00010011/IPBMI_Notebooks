import numpy as np
import os, sys
from PIL import Image

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
            coef = item[1]
            break
    if coef == 0:
        coef = np.interp(energy,[item[0] for item in data], [item[1] for item in data])
    return coef

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE

def interactor_CT(N0, obj, zPos, nProjections):
  slice = obj[:, zPos, :]
  angles = np.linspace(0, 360, nProjections, endpoint=False)
  sinograma = np.full((nProjections, slice.shape[1] * 2), N0)
  offset = int(slice.shape[1] // 2)
  img = Image.fromarray(slice)
  for i, angle in enumerate(angles):
    rotated_img = img.rotate(angle)
    projection_coef = np.sum(rotated_img, axis=0)
    projection = N0 * np.exp(-projection_coef / projection_coef.shape[0])
    sinograma[i, offset:offset + slice.shape[1]] = projection

  return sinograma

def detectorSinogram(qImage, nProjections, nDetectors):
  detected_img = np.zeros((nProjections, nDetectors))
  for i in range(nProjections):
    line = detector_1D(qImage, i, nDetectors)
    detected_img[i, :] = line
  return detected_img

def detector_1D(qImage, angle, nDetectors):
  start = int(qImage.shape[1] / 2 - nDetectors / 2)
  end = int(qImage.shape[1] / 2 + nDetectors / 2)
  detected_line = qImage[angle,start: end ]
  return detected_line


def process_CT(image, N0):
    compensated_sinogram = -np.ln(image / N0)
    return compensated_sinogram

