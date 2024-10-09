import numpy as np

def createQuantumImage(N0, n, pointSize):
  N1 = N0 * pointSize
  quantum_image = np.random.uniform(N1, n)
  return quantum_image