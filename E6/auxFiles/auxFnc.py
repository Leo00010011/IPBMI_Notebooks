import numpy as np
import os, sys
from PIL import Image

TISSUE_LABEL = {0: 'Adipose',
                1: 'Air',
                2: 'Bone',
                3: 'Breast',
                4: 'Soft',
                5: 'Water'}


def get_csv_data(tissue_index, csv_path=None):
    if not csv_path:
        csv_path = os.path.join(
            sys.path[0], 'auxFiles', 'coef', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
    else:
        csv_path = os.path.join(
            csv_path, 'coef', 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
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
    photon_distribution = np.zeros(len(qImage.flatten()), dtype=int)
    for photon_count in qImage.flatten():
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

def detector_QDE(imgData, n, m, QDE):
  original_total_photons = np.sum(imgData)
  target_total_photons = original_total_photons * QDE
  img_pil = Image.fromarray(imgData)
  
  img_resized_pil = img_pil.resize((n, m), resample=Image.BOX)
  img_resized_array = np.asarray(img_resized_pil)

  resized_total_photons = np.sum(img_resized_array)

  scaling_factor = target_total_photons / resized_total_photons
  img_detector = img_resized_array * scaling_factor
  return img_detector

def detectorNoiseFullP_QDE(image, n, m, QDE):
    # Ensure the input image is a numpy array
    img_data = np.array(image)
    
    # Scale the image data to simulate a higher photon count
    img_data = img_data * 10
    
    # Apply Poisson noise based on quantum efficiency
    img_data_after_QDE = np.random.poisson(img_data * QDE)
    
    # Convert to uint8 for image manipulation (after scaling back down)
    img_data_after_QDE = (img_data_after_QDE / 10).astype(np.uint32)
    
    # Convert numpy array to PIL Image
    img_pil = Image.fromarray(img_data_after_QDE)
    
    # Resize the image to n x m
    img_resized_pil = img_pil.resize((n, m), resample=Image.BOX)

    original_num = np.sum(img_data_after_QDE)
    target_num = np.sum((image * QDE))
    now_num = np.sum(img_resized_pil)
    scaling = target_num / now_num

    # Convert back to numpy array
    img_resized_array = np.asarray(img_resized_pil * scaling)
    
    return img_resized_array

def getSNR(image, x0, y0, w):
    region = image[x0: x0 + w,y0: y0 + w]
    return np.mean(region)/np.std(region)