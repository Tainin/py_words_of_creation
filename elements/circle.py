from utils import *
from layout import *

class Circle():
    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop('branch')
        self.radius = kwargs.pop('radius')
        padding = kwargs.pop('padding')
        
        vector = direction_to_vector(self.branch.direction)
        self.center = self.branch.origin + (vector * self.radius)

        self.box = BoxCollider(
            rect = [self.center + direction_to_vector(d) *
                    (self.radius + padding) for d in range(4)]
        )

        self.branches = [
            BranchOption(
                parent = self, direction = d,
                branch_type = get_branch_type(d, self.branch.direction),
                origin = self.center + direction_to_vector(d) * self.radius
            ) for d in range(4)
        ]

    def draw(self, drawing, line_properties):
        drawing.add(drawing.circle(self.center.tolist(),
                                   self.radius,
                                   fill = 'none',
                                   **line_properties))
        
