from layout import *
from utils import *
from elements import *

import random
import svgwrite as svg
import aabbtree as aabb

padding = 19

def gen_circle(option):
    return Circle(branch = option, radius = random.uniform(10, 80), padding = padding)

def gen_line(option):
    return LineSegment(branch = option, length = random.uniform(75, 300), padding = padding)

def gen_perpendicular_diamond(option):
    minor_radius = random.uniform(15, 40)
    return PerpendicularDiamond(branch = option, minor_radius = minor_radius, major_radius = minor_radius * 7, padding = padding)

bounds = [0, 0, 8000, 8000]

network_1 = Network(
    area = CompoundArea(
        sub_areas = [
            InsetArea(
                outer_area = RectangularArea(points = [np.array(point) for point in points]),
                inset_distance = 900
            ) for points in [[[0, 0], [6000, 3000]], [[0, 0], [3000, 6000]]]
        ]
    )
)

network_2 = Network(
    area = CompoundArea(
        sub_areas = [
            InsetArea(
                outer_area = RectangularArea(points = [np.array(point) for point in points]),
                inset_distance = 900
            ) for points in [[[8000, 8000], [2000, 5000]], [[8000, 8000], [5000, 2000]]]
        ]
    )
)

layer_area = RectangularArea(points = [np.array([0, 0]), np.array([8000, 8000])])
networks = [network_1, network_2]
tree = aabb.AABBTree()

count = 0
goal_count = 1000
while count < goal_count:
    network = random.choice(networks)
    index = random.randint(0, len(network.frontier) - 1)
    network.frontier[index], network.frontier[-1] = network.frontier[-1], network.frontier[index] # swap a random index to the end
    option = network.frontier.pop()

    if option.branch_type is BranchType.Perpendicular and random.random() < 0.45 and len(network.frontier) > 2:
        continue

    if option.branch_type is BranchType.Forward and random.random() < 0.01 and len(network.frontier) > 2:
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

network_1.area.draw_area(annotated, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(255,0,0,'rgb'),})
network_2.area.draw_area(annotated, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(255,0,0,'rgb'),})


plain.save()
annotated.save()
