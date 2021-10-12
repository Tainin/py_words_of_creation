from utils import *
from layout import *

def get_line_segment_rect(start, end, padding):
    def get_vector(direction):
        return direction_to_vector(direction) * padding
    def get_padded_endpoint_rect(endpoint):
        return [endpoint + get_vector(direction) for direction in range(4)]
    return get_padded_endpoint_rect(start) + get_padded_endpoint_rect(end)

class LineSegment():
    def __init__(self, *args, **kwargs):
        self.branch = kwargs.pop('branch')
        self.length = kwargs.pop('length')
        padding = kwargs.pop('padding')

        vector = direction_to_vector(self.branch.direction)
        self.end = self.branch.origin + (vector * self.length)

        self.box = BoxCollider(
            rect = get_line_segment_rect(self.branch.origin, self.end, padding)
        )

    def draw(self, drawing, line_properties):
        drawing.add(drawing.line(self.branch.origin.tolist(),
                                 self.end.tolist(),
                                 **line_properties,
                                 stroke_linecap = 'square'))

    def get_branch_options(self):
        forward = BranchOption(
            origin = self.end,
            direction =  self.branch.direction,
            parent = self
        )
        return [forward]
