import random

class CompoundArea():
    def __init__(self, *args, **kwargs):
        self.sub_areas = kwargs.pop('sub_areas')

    def all_boxes(self):
        return (box for area in self.sub_areas for box in area.all_boxes())

    def does_element_overlap(self, element):
        return any(area.does_element_overlap(element)
                   for area in self.sub_areas)

    def draw_area(self, drawing, line_properties):
        for area in self.sub_areas:
            area.draw_area(drawing, line_properties)

    def get_random_point(self):
        area = random.choice(self.sub_areas)
        return area.get_random_point()
