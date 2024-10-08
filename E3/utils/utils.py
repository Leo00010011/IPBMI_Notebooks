import os
import sys
import numpy as np

TISSUE_LABEL = {0: 'Adipose',
                1: 'Air',
                2: 'Bone',
                3: 'Breast',
                4: 'Soft',
                5: 'Water'}

ADIPOSE_INDEX = 0
AIR_INDEX = 1
BONE_INDEX = 2
BREAST_INDEX = 3
SOFT_INDEX = 4
WATER_INDEX = 5


SOURCE_PATH = 'C:\\Users\\ulloa\\Miooooo\\Master\\IPBMA\\IPBMANotebooks\\IPBMI_Notebooks\\E3\\auxFiles'



class EnergyCoef:
    tissue_coefs = {
        'Adipose': None,
        'Air': None,
        'Bone': None,
        'Breast': None,
        'Soft': None,
        'Water': None
    }

    def __init__(self, csv_path= None) -> None:
      if not csv_path:
        self.csv_path = os.path.join(sys.path[0], 'auxFiles')
      else:
        self.csv_path = csv_path

    def normalize_data(data):
        return np.round(data/data.max(), 2) * 256


    def getLine(data, nLine):
        lines = data[:, nLine]
        return lines
    
    def get_csv_data(self,tissue_index, csv_path=None):
        data = EnergyCoef.tissue_coefs[TISSUE_LABEL[tissue_index]]
        if data:
           return data  
        data = dict()
        csv_path = os.path.join(self.csv_path, 'coefAtenuacion' + TISSUE_LABEL[tissue_index] + '.csv')
        with open(csv_path, 'r') as file:
            next(file)
            next(file)
            for line in file:
                line = line.strip().split('\t')
                data[float(line[0])] = line[1] 
        EnergyCoef.tissue_coefs[TISSUE_LABEL[tissue_index]] = data
        return data


    def get_coef(self, tissue, energy, csv_path=None):
        data: = self.get_csv_data(tissue, csv_path)
        coef = 
        
        return coef

db = EnergyCoef(SOURCE_PATH)

print(db.get_coef(3,40, SOURCE_PATH))

