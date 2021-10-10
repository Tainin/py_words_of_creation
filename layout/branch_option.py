import numpy as np

from utils import *

class BranchOption():
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent')
        self.origin = np.array(kwargs.pop('origin'))
        self.direction = constrain_direction(kwargs.pop('direction'))
        self.element = None
