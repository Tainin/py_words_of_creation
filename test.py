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
    return LineSegment(branch = option, length = random.uniform(50, 200), padding = padding)

def gen_perpendicular_diamond(option):
    minor_radius = random.uniform(15, 40)
    return PerpendicularDiamond(branch = option, minor_radius = minor_radius, major_radius = minor_radius * 7, padding = padding)

bounds = [0, 0, 8000, 8000]
area = BoxCollider(rect = np.array([bounds[:2:], bounds[2::]]))
tree = aabb.AABBTree()

initial_option = BranchOption(
    parent = None,
    origin = (4000, 4000),
    direction = constrain_direction(random.randint(0,10000)),
    branch_type = BranchType.Forward
)

options = [initial_option]

count = 0
while count < 2000:
    index = random.randint(0, len(options) - 1)
    options[index], options[-1] = options[-1], options[index] # swap a random index to the end
    option = options.pop()
    if random.random() < 0.1 and len(options) > 2:
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
    
    if element.box.overlaps_with(area) and len(element.box.get_overlapping(tree)) <= 1:
        option.element = element
        tree.add(element.box.box, element)
        options += element.branches
        count += 1
    else:
        options.append(option)

    option_count = len(options)

    if (count % 100) == 0:
        print("Elements: " + str(count))
        print("Options: " + str(option_count))
        print()
    

plain = svg.Drawing("test.svg", ('20cm', '20cm'))
plain.viewbox(*bounds)

annotated = svg.Drawing("test_annotated.svg", ('20cm', '20cm'))
annotated.viewbox(*bounds)

all_elements = area.get_overlapping(tree)
for element in all_elements:
    element.draw(plain, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})
    element.draw(annotated, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})
for element in all_elements:
    element.box.draw_box(annotated, line_properties = {'stroke_width': 3, 'stroke': svg.rgb(255,0,0,'rgb'),})

plain.save()
annotated.save()
