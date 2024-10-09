import numpy as np

def createQuantumImage(N0, n, pointSize):
  N1 = N0 * (pointSize ** 2)
  quantum_image = np.random.poisson(N1, n)
  return quantum_image