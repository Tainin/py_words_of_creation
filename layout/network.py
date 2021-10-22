import random

from layout import *
from utils import *

class Network():
    def __init__(self, *args, **kwargs):
        self.area = kwargs.pop('area')
        self.frontier = [
            BranchOption(
                parent = None,
                origin = self.area.get_random_point(),
                direction = constrain_direction(random.randint(0,10000)),
                branch_type = BranchType.Forward
            )
        ]
