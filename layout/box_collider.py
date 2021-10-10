from aabbtree import *

class BoxCollider():
    def __init__(self, *args, **kwargs):
        rect = kwargs.pop('rect') # rect must be of form [[x1, y1], [x2, y2]...]
        rect = zip(*rect) # rearrange rect to [[x1, x2...], [y1, y2...]]
        rect = tuple((min(pair), max(pair)) for pair in rect) # rearrange rect to [[minX, maxX], [minY, maxY]]
        self.box = AABB(rect)

    def overlaps_with(self, other):
        return self.box.overlaps(other.box)

    def get_overlapping(self, box_tree):
        return box_tree.overlap_values(self.box)
