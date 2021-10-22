from layout import *
import random
import numpy as np

class RectangularArea():
    def __init__(self, *args, **kwargs):
        points = kwargs.pop('points')

        self.box = BoxCollider(rect = points)

    def all_boxes(self):
        yield self.box

    def does_element_overlap(self, element):
        return self.box.overlaps_with(element.box)

    def draw_area(self, drawing, line_properties):
        self.box.draw_box(drawing, line_properties)

    def get_random_point(self):
        point = [random.uniform(n, x) for n, x in self.box.box.limits]
        return np.array(point)
