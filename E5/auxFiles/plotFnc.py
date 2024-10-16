import matplotlib.pyplot as plt

def plotLineH(qImage, line):
  lines = qImage[line, :]
  plt.plot(lines)