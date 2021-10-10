import numpy as np
from math import sin, cos, pi

def constrain_direction(direction):
    return round(direction) % 4

def direction_to_vector(direction):
    angle = constrain_direction(direction) * (pi / 2)
    return np.array((round(cos(angle)), round(sin(angle))))

def vector_to_direction(vector):
    angle = np.arctan2(*vector[::-1])
    angle *= 2 / pi
    return constrain_direction(angle)
