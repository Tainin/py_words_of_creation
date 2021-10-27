from layout import *
from utils import *
from elements import *

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

def get_circle_networks():
    return [Network(area = get_circle_area(np.array([4000, 4000]), 3500, 15))]

def attempt_element_generation(option):
    if option.parent is None:
        return True

    if option.direction % 2 == 1 and random.random() < 0.95:
        return True
    if option.direction == option.parent.branch.direction and random.random() < 0.55:
        return True
    if random.random() < 0.001:
        return True
    return False

bounds = [0, 0, 8000, 8000]
layer_area = RectangularArea(points = [np.array([0, 0]), np.array([8000, 8000])])
#networks = get_corner_networks()
networks = get_circle_networks()
tree = aabb.AABBTree()

count = 0
goal_count = 1100
last_percent = 1
while count < goal_count:
    network = random.choice(networks)
    index = random.randint(0, len(network.frontier) - 1)
    network.frontier[index], network.frontier[-1] = network.frontier[-1], network.frontier[index] # swap a random index to the end
    option = network.frontier.pop()

    if not attempt_element_generation(option):
        if len(network.frontier):
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

    if network.area.does_element_overlap(element) and len(element.box.get_overlapping(tree)) <= 1:
        option.element = element
        tree.add(element.box.box, element)
        network.frontier += element.branches
        count += 1
    else:
        network.frontier.append(option)

    percent = float(count) / goal_count * 100
    if percent - last_percent > 1.0:
        print(str(count) + " / " + str(goal_count) + " = " + str(int(percent)) + "%")
        last_percent = percent
    

plain = svg.Drawing("test.svg", ('20cm', '20cm'))
plain.viewbox(*bounds)

annotated = svg.Drawing("test_annotated.svg", ('20cm', '20cm'))
annotated.viewbox(*bounds)

all_elements = layer_area.box.get_overlapping(tree)
for element in all_elements:
    element.draw(plain, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})
    element.draw(annotated, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})
for element in all_elements:
    element.box.draw_box(annotated, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(255,0,0,'rgb'),})
    for branch in element.branches:
        branch.draw_branch(annotated, 50, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(0,255,0,'rgb'),})

for network in networks:
    network.area.draw_area(annotated, line_properties = {'stroke_width': 5, 'stroke': svg.rgb(0,255,0,'rgb'),})

plain.save()
annotated.save()
