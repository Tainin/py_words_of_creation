from layout import *
import random
import numpy as np

class InsetArea():
    def __init__(self, *args, **kwargs):
        inset_distance = kwargs.pop('inset_distance')
        self.outer = kwargs.pop('outer_area')

        limits = ((n + inset_distance, x - inset_distance)
                  for n, x in self.outer.box.box.limits)
        limits = zip(*limits)
        points = [np.array(point) for point in limits]
        self.box = BoxCollider(rect = points)

    def all_boxes(self):
        yield self.box

    def does_element_overlap(self, element):
        return self.box.overlaps_with(element.box)

    def draw_area(self, drawing, line_properties, line_modifiers = {}):
        self.box.draw_box(drawing, line_properties)
        self.outer.box.draw_box(drawing, line_properties | line_modifiers)

    def get_random_point(self):
        point = [random.uniform(n, x) for n, x in self.box.box.limits]
        return np.array(point)
