from layout import *
from utils import *
from elements import *

import random
import svgwrite as svg
import aabbtree as aabb

bounds = [0, 0, 2000, 2000]
area = BoxCollider(rect = [bounds[:2:], bounds[2::]])
tree = aabb.AABBTree()

initial_option = BranchOption(
    origin = (1000, 1000),
    direction = constrain_direction(random.randint(0,10000)),
    parent = None
)

options = [initial_option]

count = 0
while count < 300:
    index = random.randint(0, len(options) - 1)
    options[index], options[-1] = options[-1], options[index] # swap a random index to the end
    option = options.pop()

    element = Circle(
        branch = option,
        padding = 5,
        radius = random.uniform(10, 80),
    )
    
    if element.box.overlaps_with(area) and len(element.box.get_overlapping(tree)) <= 1:
        tree.add(element.box.box, element)
        new_options = element.get_branch_options()
        options.append(new_options[0])
        options.append(new_options[1][0])
        options.append(new_options[1][1])
        count += 1
    elif len(options) <= 1:
        options.append(option)

dwg = svg.Drawing("test.svg", ('20cm', '20cm'))
dwg.viewbox(*bounds)
for element in area.get_overlapping(tree):
    element.draw(dwg, line_properties = {'stroke_width': 9, 'stroke': svg.rgb(0,0,0,'rgb'),})

dwg.save()
