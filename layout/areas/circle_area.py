from math import sin, cos, pi

import numpy as np

from . import CompoundArea, RectangularArea

def get_circle_area(center, radius, resolution):
    rects = range(1,resolution)
    rects = ((angle * pi) / (2 * resolution) for angle in rects)
    rects = (np.array([cos(angle), sin(angle)]) for angle in rects)
    rects = ([center + point * radius, center - point * radius]
              for point in rects)
    
    return CompoundArea(
        sub_areas = [
            RectangularArea(points = points) for points in rects
        ]
    )
                
