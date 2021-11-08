from .areas import RectangularArea
from utils import *

import numpy as np
import svgwrite as svg
import aabbtree as aabb

class Layer():
    def __init__(self, *args, **kwargs):
        self.bounds = kwargs.pop('bounds')
        self.area = RectangularArea(
            points = [
                np.array(self.bounds[:2:]),
                np.array(self.bounds[2::])
            ]
        )
        self.tree = aabb.AABBTree()
        self.networks = []

    def all_elements(self):
        return self.area.box.get_overlapping(self.tree)

    def get_drawing(self, name):
        drawing = svg.Drawing(name + ".svg", ('100%', '100%'))
        drawing.viewbox(*self.bounds)
        return drawing

    def draw(self, drawing, line_properties, draw_options = {}):
        for element in self.all_elements():
            element.draw(drawing, line_properties['lines'])
            if draw_options.get('boxes', False):
                element.box.draw_box(drawing, line_properties['boxes'])
            if draw_options.get('branches', False):
                for branch in element.branches:
                    branch.draw_branch(drawing, 50, line_properties['branches'])

        if draw_options.get('networks', False):
            for network in self.networks:
                network.area.draw_area(drawing, line_properties['networks'])

        if draw_options.get('layer_area', False):
            self.area.draw_area(drawing, line_properties['layer_area'])
