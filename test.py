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

area_1 = RectangularArea(points = np.array([[0, 0], [8000, 4000]]))
area_1 = InsetArea(outer_area = area_1, inset_distance = 500)

print("Area_1: " + str(area_1.box.box.limits))

area_2 = RectangularArea(points = np.array([[0, 4000], [8000, 8000]]))
area_2 = InsetArea(outer_area = area_2, inset_distance = 500)

print("Area_2: " + str(area_2.box.box.limits))

area = CompoundArea(sub_areas = [area_1, area_2])

for box in area.all_boxes():
    print(box.box.limits)

tree = aabb.AABBTree()

options = [
    BranchOption(
        parent = None,
        origin = a.get_random_point(),
        direction = constrain_direction(random.randint(0,10000)),
        branch_type = BranchType.Forward
    ) for a in [area_1, area_2]
]
    

count = 0
goal_count = 700
previous_count = -1
while count < goal_count:
    index = random.randint(0, len(options) - 1)
    options[index], options[-1] = options[-1], options[index] # swap a random index to the end
    option = options.pop()

    if option.branch_type is BranchType.Perpendicular and random.random() < 0.65 and len(options) > 2:
        continue

    if option.branch_type is BranchType.Forward and random.random() < 0.01 and len(options) > 2:
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

    if area.does_element_overlap(element) and len(element.box.get_overlapping(tree)) <= 1:
        option.element = element
        tree.add(element.box.box, element)
        options += element.branches
        count += 1
    else:
        options.append(option)

    if count == previous_count:
        repeat += 1
    else:
        repeat = 1
    previous_count = count

    if repeat >= 2:
        print("Elements: " + str(count) + " Open options: " + str(len(options)) + " Repeated: " + str(repeat) + " times")
    

plain = svg.Drawing("test.svg", ('20cm', '20cm'))
plain.viewbox(*bounds)

annotated = svg.Drawing("test_annotated.svg", ('20cm', '20cm'))
annotated.viewbox(*bounds)

all_elements = sum([box.get_overlapping(tree) for box in area.all_boxes()], [])
for element in all_elements:
    element.draw(plain, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})
    element.draw(annotated, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})
for element in all_elements:
    element.box.draw_box(annotated, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(255,0,0,'rgb'),})
    for branch in element.branches:
        branch.draw_branch(annotated, 50, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(0,255,0,'rgb'),})

area.draw_area(annotated, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(255,0,0,'rgb'),})

plain.save()
annotated.save()
