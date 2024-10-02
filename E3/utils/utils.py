import os
import sys 
import numpy as np

def read_csv(fileName):
  csv_path = os.path.join(sys.path[0], 'auxFiles', fileName)
  fr = open(csv_path)
  lines = fr.readlines()
  dataArr = []
  for line in lines:
    listFromLine = line.strip().split('\t')
    dataArr.append(listFromLine)

  return dataArr[2:]