from utils import *
from layout import *

class Circle():
    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop('branch')
        self.radius = kwargs.pop('radius')
        padding = kwargs.pop('padding')
        
        vector = direction_to_vector(self.branch.direction)
        self.center = self.branch.origin + (vector * self.radius)
        
        data = ((d, direction_to_vector(d)) for d in range(4))
        data = ((d, vec * self.radius, vec * (self.radius + padding))
                for d, vec in data)
        data = ((d, self.center + vec, self.center + padded_vec)
                for d, vec, padded_vec in data)
        data = ((padded_point,
                 create_option(self, point, d, self.branch.direction))
                for d, point, padded_point in data)

        data = zip(*data)
        self.box = BoxCollider(rect = next(data))
        self.branches = next(data)

    def draw(self, drawing, line_properties):
        drawing.add(drawing.circle(self.center.tolist(),
                                   self.radius,
                                   fill = 'none',
                                   **line_properties))
        
