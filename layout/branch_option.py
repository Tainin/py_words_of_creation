import numpy as np

from utils import *

from enum import Enum, auto, unique

@unique
class BranchType(Enum):
    Forward = auto()
    Perpendicular = auto()

def get_branch_type(direction, forward_direction):
    if direction == forward_direction:
        return BranchType.Forward
    else:
        return BranchType.Perpendicular

class BranchOption():
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent')
        self.origin = np.array(kwargs.pop('origin'))
        self.direction = constrain_direction(kwargs.pop('direction'))
        self.branch_type = kwargs.pop('branch_type')
        self.element = None
