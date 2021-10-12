from aabbtree import *

class BoxCollider():
    def __init__(self, *args, **kwargs):
        rect = [point.tolist() for point in kwargs.pop('rect')] # rect must be of form [[x1, y1], [x2, y2]...]
        rect = zip(*rect) # rearrange rect to [[x1, x2...], [y1, y2...]]
        rect = tuple((min(pair), max(pair)) for pair in rect) # rearrange rect to [[minX, maxX], [minY, maxY]]
        self.box = AABB(rect)

    def overlaps_with(self, other):
        return self.box.overlaps(other.box)

    def get_overlapping(self, box_tree):
        return box_tree.overlap_values(self.box)

    def draw_box(self, drawing, line_properties):
        rect_data = [(p[0], p[1] - p[0] + 1) for p in self.box.limits]
        rect_data = tuple(zip(*rect_data))
        drawing.add(drawing.rect(*rect_data, fill='none', **line_properties))
