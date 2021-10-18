from layout import box_collider
import random
import numpy as np

class InsetArea():
    def __init__(self, *args, **kwargs):
        inset_distance = kwargs.pop('inset_distance')
        self.outer = kwargs.pop('outer_area')

        points = [(n + inset_distance, x - inset_distance)
                  for n, x in self.outer.box.limits]
        self.box = BoxCollider(rect = points)

    def all_boxes(self):
        yield self.box

    def does_element_overlap(self, element):
        return self.box.overlaps_with(element.box)

    def draw_area(self, drawing, line_properties):
        self.box.draw_box(drawing, line_properties)
        dotted_line_properties = line_properties.copy()
        dash_length = dotted_line_properties['stroke_width'] * 4
        dotted_line_properties['stroke_dasharray'] = dash_length
        self.outer.box.draw_box(drawing, dotted_line_properties)

    def get_random_point(self):
        point = [random.uniform(n, x) for n, x in self.box.limits]
        return np.array(point)
