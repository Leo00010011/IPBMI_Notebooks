import numpy as np

def createQuantumImage(N0, n, pointSize):
  N1 = N0 * (pointSize ** 2)
  quantum_image = np.full((int(np.sqrt(n)), int(np.sqrt(n))), N1)
  return quantum_image

def insertNoduleQImage(imgData, noduleSize, noduleContrast):
  large_edge = imgData.shape[0]
  insert_edge = large_edge * 0.01 * noduleSize
  insert_radius = int(insert_edge / 2)
  nodule_value = np.mean(imgData) * 0.01 * noduleContrast
  # create a circle
  noduleImage = imgData.copy()
  start_offset = int(large_edge / 2)
  x = np.arange(large_edge)
  y = np.arange(large_edge)
  cx = start_offset - 0.5
  cy = start_offset - 0.5
  r = insert_radius
  mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < r**2
  noduleImage[mask] = nodule_value

  return noduleImage
