import numpy as np

from utils import *

from enum import Enum, auto, unique

@unique
class BranchType(Enum):
    Initial = auto()
    Reverse = auto()
    Capped = auto()
    Forward = auto()
    Perpendicular = auto()

class BranchOption():
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent')
        self.origin = np.array(kwargs.pop('origin'))
        self.direction = constrain_direction(kwargs.pop('direction'))
        self.branch_type = kwargs.pop('branch_type')
        self.element = None

branch_types = {0: BranchType.Forward, 2: BranchType.Reverse}

def create_option(parent, origin, direction, forward):
    return BranchOption(
        parent = parent, origin = origin, direction = direction,
        branch_type = branch_types.get(
            constrain_direction(direction - forward),
            BranchType.Perpendicular
        )
    )
