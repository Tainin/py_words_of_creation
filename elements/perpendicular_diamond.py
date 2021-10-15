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
        data = ((d, vec, choose_radius(self.radii, d, self.branch.direction))
                for d, vec in data)
        data = ((d, vec * radius, vec * (radius + padding))
                for d, vec, radius in data)
        data = ((d, self.center + vec, self.center + padded_vec)
                for d, vec, padded_vec in data)
        data = ((point, padded_point,
                 create_option(self, point, d, self.branch.direction))
                for d, point, padded_point in data)

        data = zip(*data)
        self.points = next(data)
        self.box = BoxCollider(rect = next(data))
        self.branches = next(data)

    def draw(self, drawing, line_properties):
        drawing.add(drawing.polygon([point.tolist() for point in self.points],
                                    fill = 'none', **line_properties))
