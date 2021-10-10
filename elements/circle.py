from utils import *
from layout import *

def get_circle_rect(center, radius, padding):
    def get_vector(direction):
        return direction_to_vector(direction) * (radius + padding)
    return [center + get_vector(direction) for direction in range(4)]
    
class Circle():
    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop('branch')
        self.radius = kwargs.pop('radius')
        padding = kwargs.pop('padding')
        
        vector = direction_to_vector(self.branch.direction)
        self.center = self.branch.origin + (vector * self.radius)
        
        self.box = BoxCollider(
            rect = get_circle_rect(self.center, self.radius, padding)
        )

    def draw(self, drawing, line_properties):
        drawing.add(drawing.circle(self.center.tolist(),
                                   self.radius,
                                   fill = 'none',
                                   **line_properties))

    def get_branch_options(self):
        def generate_option(direction):
            return BranchOption(
                origin = self.center + (direction_to_vector(direction) * self.radius),
                direction = direction,
                parent = self
            )

        forward = generate_option(self.branch.direction)
        perpendiculars = [generate_option(constrain_direction(self.branch.direction + turn)) for turn in [-1, 1]]
        return [forward, perpendiculars]
        
