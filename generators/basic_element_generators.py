from elements import *

import random

def get_circle_generator(min_radius, max_radius, padding):
    def invoke(option):
        return Circle(
            branch = option,
            radius = random.uniform(min_radius, max_radius),
            padding = padding
        )
    return invoke

def get_line_generator(min_length, max_length, padding):
    def invoke(option):
        return LineSegment(
            branch = option,
            length = random.uniform(min_length, max_length),
            padding = padding
        )
    return invoke

def get_diamond_generator(min_minor_radius, max_minor_radius, major_radius_scale, padding):
    def invoke(option):
        minor_radius = random.uniform(min_minor_radius, max_minor_radius)
        return PerpendicularDiamond(
            branch = option,
            minor_radius = minor_radius,
            major_radius = minor_radius * major_radius_scale,
            padding = padding
        )
    return invoke
