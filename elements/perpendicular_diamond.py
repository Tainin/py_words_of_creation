from utils import *
from layout import *

def choose_radius(radii, direction, forward):
    return radii[constrain_direction(direction - forward) % 2]

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
        
        data = ((d, direction_to_vector(d)) for d in range(4))
        data = ((vector, choose_radius(self.radii, d, self.branch.direction)) for d, vector in data)
        data = ((vector, radius, radius + padding) for vector, radius in data)
        data = ((vector * radius, vector * padded_radius) for vector, radius, padded_radius in data)
        data = ((self.center + vector, self.center + padded_vector) for vector, padded_vector in data)

        data = zip(*data)
        self.points = next(data)
        self.box = BoxCollider(rect = next(data))

        branch_directions = (self.branch.direction + turn
                             for turn in (-1, 0, 1))

        self.branches = [
            BranchOption(
                parent = self, direction = d,
                branch_type = get_branch_type(d, self.branch.direction),
                origin = self.center + direction_to_vector(d) *
                    choose_radius(self.radii, d, self.branch.direction)
            ) for d in branch_directions
        ]

    def draw(self, drawing, line_properties):
        drawing.add(drawing.polygon([point.tolist() for point in self.points],
                                    fill = 'none', **line_properties))
