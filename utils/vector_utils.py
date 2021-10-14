import numpy as np

def normalized(vector):
    return vector / np.sqrt(np.sum(np.power(vector, 2)))
