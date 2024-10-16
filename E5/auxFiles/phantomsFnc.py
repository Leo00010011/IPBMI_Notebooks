import numpy as np

def source(Kpv, I0):
  N0 = I0
  eE = Kpv * 0.4
  return N0, eE