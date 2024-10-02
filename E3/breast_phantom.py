def lin_coef(tissue: str, energy, source_path:str):
    tissue_label = {'adipose': 1,
    'air': 2,
    'bone': 3,
    'breast': 4,
    'soft': 5,
    'water': 6}
    return tissue_label[tissue]

def breast_phantom(edge_size, energy):
    