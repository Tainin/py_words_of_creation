from utils import *
from layout import *

def is_minor_direction(direction, forward):
    return (direction % 2) == (forward % 2)

def get_reletive_point(direction, radii, forward):
    radius = radii[0] if is_minor_direction(direction, forward) else radii[1]
    return direction_to_vector(direction) * radius

class PerpendicularDiamond():
    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop('branch')
        self.radii = [
            kwargs.pop('minor_radius'),
            kwargs.pop('major_radius')
        ]
        padding = kwargs.pop('padding')

        vector = direction_to_vector(self.branch.direction)
        self.center = self.branch.origin + (vector * self.radii[0])

        self.points = [get_reletive_point(
                self.branch.direction + turn,
                self.radii, self.branch.direction
            ) for turn in range(4)
        ]

        self.box = BoxCollider(
            rect = [self.center + point + normalized(point) * padding for point in self.points]
        )

    def draw(self, drawing, line_properties):
        drawing.add(drawing.polygon([(self.center + point).tolist() for point in self.points],
                                    fill = 'none',
                                    **line_properties))

    def get_branch_options(self):
        def generate_option(direction):
            return BranchOption(
                origin = self.center + get_reletive_point(
                    direction, self.radii, self.branch.direction),
                direction = direction,
                parent = self
            )

        forward = generate_option(self.branch.direction)
        perpendiculars = [
            generate_option(constrain_direction(self.branch.direction + turn))
            for turn in [-1, 1]
        ]
        return [forward, perpendiculars]
            
