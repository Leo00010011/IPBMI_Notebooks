import matplotlib.pyplot as plt

def plotLineH(qImage, line):
  lines = qImage[line, :]
  plt.ylim(0, max(lines) + 10)
  plt.xlim(0, len(lines))
  plt.xlabel("X Position")
  plt.ylabel("GL Value")
  plt.plot(lines)

def plotDistribution(hist, xLabel, yLabel):
  plt.xlabel(xLabel)
  plt.ylabel(yLabel)
  plt.plot(hist[0])