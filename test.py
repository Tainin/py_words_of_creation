from layout import *
from utils import *
from elements import *

import sys
import random
import svgwrite as svg
import aabbtree as aabb

padding = 25

def gen_circle(option):
    return Circle(branch = option, radius = random.uniform(30, 120), padding = padding)

def gen_line(option):
    return LineSegment(branch = option, length = random.uniform(75, 500), padding = padding)

def gen_perpendicular_diamond(option):
    minor_radius = random.uniform(15, 40)
    return PerpendicularDiamond(branch = option, minor_radius = minor_radius, major_radius = minor_radius * 7, padding = padding)

def get_corner_rects(corner, inwards_vector, width, length):
    return [
        [corner, corner + inwards_vector * np.array([width, length])],
        [corner, corner + inwards_vector * np.array([length, width])]
    ]

def get_corner_networks():
    return [
        Network(
            area = CompoundArea(
                sub_areas = [
                    InsetArea(
                        outer_area = RectangularArea(points = rect),
                        inset_distance = 500
                    ) for rect in get_corner_rects(corner, inwards, 2500, 6000)
                ]
            )
        ) for corner, inwards in [(np.array([0,0]), np.array([1,1])), (np.array([8000,8000]), np.array([-1,-1]))]
    ]

def get_edge_rect(origin, in_direction, width, length):
    in_vector = direction_to_vector(in_direction)
    edge_vector = direction_to_vector(in_direction + 1)

    x = [origin - (edge_vector * (length / 2)), origin + (edge_vector * (length / 2)) + (in_vector * width)]
    print(x)
    return x

def get_frame_networks():
    return [
        Network(
            area = InsetArea(
                outer_area = RectangularArea(points = get_edge_rect(origin, inwards, 2000, 6000)),
                inset_distance = 500
            )
        ) for origin, inwards in [(np.array([0,4000]), 0), (np.array([4000,0]), 1), (np.array([8000,4000]), 2), (np.array([4000,8000]), 3)]
    ]

def get_vert_bars_networks():
    return [
        Network(
            area = InsetArea(
                outer_area = RectangularArea(points = get_edge_rect(origin, inwards, 2000, 6000)),
                inset_distance = 500
            )
        ) for origin, inwards in [(np.array([0,4000]), 0), (np.array([8000,4000]), 2)]
    ]
    

def get_circle_networks():
    return [Network(area = get_circle_area(np.array([4000, 4000]), 2500, 15))]

def get_rect_networks():
    return [
        Network(
            area = InsetArea(
                outer_area = RectangularArea(points = rect),
                inset_distance = 500
            )
        ) for rect in [(np.array([0,0]), np.array([8000,4000])), (np.array([0,4000]), np.array([8000,8000]))]
    ]

def get_full_layer_networks():
    return [
        Network(
            area = InsetArea(
                outer_area = RectangularArea(points = [np.array([0,0]), np.array([8000,8000])]),
                inset_distance = 500
            )
        )
    ]

def attempt_element_generation(option):
    if option.parent is None:
        return True

    if option.direction % 2 == 1 and random.random() < 0.91:
        return True
    if option.direction == option.parent.branch.direction and random.random() < 0.27:
        return True
    if random.random() < 0.001:
        return True
    return False

layer = Layer(bounds = [0, 0, 8000, 8000])

layer.networks = get_corner_networks()
#layer.networks = get_circle_networks()
#layer.networks = get_rect_networks()
#layer.networks = get_frame_networks()
#layer.networks = get_vert_bars_networks()
#layer.networks = get_full_layer_networks()

count = 0
goal_count = int(sys.argv[1])
last_percent = 1
while count < goal_count:
    network = random.choice(layer.networks)
    index = random.randint(0, len(network.frontier) - 1)
    network.frontier[index], network.frontier[-1] = network.frontier[-1], network.frontier[index] # swap a random index to the end
    option = network.frontier.pop()

    if not attempt_element_generation(option):
        network.frontier.append(option)
        continue
    
    element = random.choice([
        gen_perpendicular_diamond,
        gen_circle,
        gen_circle,
        gen_line,
        gen_line,
        gen_line,
        gen_line,
        gen_line,
        gen_line
    ])(option)

    if network.area.does_element_overlap(element) and len(element.box.get_overlapping(layer.tree)) <= 1:
        option.element = element
        layer.tree.add(element.box.box, element)
        network.frontier += element.branches
        count += 1
    else:
        network.frontier.append(option)

    percent = float(count) / goal_count * 100
    if percent - last_percent > 1.0:
        print(str(count) + " / " + str(goal_count) + " = " + str(int(percent)) + "%")
        last_percent = percent
    

plain = layer.get_drawing("test")
annotated = layer.get_drawing("test_annotated")

line_properties = {
    'lines': {
        'stroke_width': 9,
        'stroke': svg.rgb(0,0,0,'rgb'),
    },
    'boxes': {
        'stroke_width': 5,
        'stroke': svg.rgb(255,0,0,'rgb'),
    },
    'branches': {
        'stroke_width': 5,
        'stroke': svg.rgb(0,255,0,'rgb'),
    },
    'networks': {
        'stroke_width': 5,
        'stroke': svg.rgb(0,0,255,'rgb'),
    },
    'layer_area': {
        'stroke_width': 5,
        'stroke': svg.rgb(255,0,255,'rgb'),
    },
    'frontier': {
        'stroke_width': 5,
        'stroke': svg.rgb(0,0,255,'rgb'),
    },
    'areas_modifier': {
        'stroke_dasharray': 50,
    },
}

annotated_options = {
    'boxes': True,
    'branches': True,
    'networks': True,
    'layer_area': True,
    'frontier': True,
}

layer.draw(plain, line_properties)
layer.draw(annotated, line_properties, annotated_options)

plain.save()
annotated.save()
