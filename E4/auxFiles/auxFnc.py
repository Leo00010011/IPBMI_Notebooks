import numpy as np
import matplotlib.pyplot as plt

def plotMiddleLine(imgData, N1):
  line = imgData[int(imgData.shape[0] / 2), :]
  plt.plot(line)
  plt.hlines(y=N1, color='black', xmin=0, xmax=imgData.shape[1], linestyle='-')
  plt.hlines(y=N1 + (2 * np.sqrt(N1)), xmin=0, xmax=imgData.shape[1], color='black', linestyle='dashdot')
  plt.hlines(y=N1 - (2 * np.sqrt(N1)), xmin=0, xmax=imgData.shape[1], color='black', linestyle='dashdot')
  plt.ylim(N1 - (2 * np.sqrt(N1)) - 50, N1 + (2 * np.sqrt(N1)) + 50)

def plotCellDistribution(img, numberOfBins):
    hist, bin_edges = np.histogram(img, bins=numberOfBins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    plt.plot(bin_centers, hist)