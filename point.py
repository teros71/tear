import math
import random
import sys
import json

import shape
import tear

def addPolygon(points, op, color, dx, dy, da):
    f = open('polygon.svg', 'a')
#    f.write('<g transform="translate({0} {1}) rotate(380,500,{2})">\n'.format(dx, dy, da))
    f.write('<polygon\n')
    f.write('points="')
    for p in points:
        f.write('{0},{1} '.format(p.x, p.y))
    f.write('"\n')
    f.write('style="opacity:{0};fill:{1};stroke:none;stroke-width:0" />\n'.format(op, color))
#    f.write('</g>\n')
    f.close()


def generatePolygons(s):
    for i in range(s.output.count):
        pol = tear.generate(s.points, s.tear)
        addPolygon(pol, s.output.opacity, s.output.colours[i % len(s.output.colours)], -i * s.output.dx, -i * s.output.dy, i * 0)


#colors = ['aqua','springgreen','blue','cyan', 'turquoise']
colors = ['aqua','springgreen']

shapes = []
try:
    print("reading shapes")
    shapes = shape.readFromFile('golden.json')
except (ValueError, KeyError) as err:
    print("error: {0}".format(err))
    exit(1)

f = open('polygon.svg', 'w')
f.write('<svg height="900" width="1400" xmlns="http://www.w3.org/2000/svg">\n')
f.close()


print("generating")
for s in shapes:
    generatePolygons(s)


#for p in newps:
#    p.output()
#print(len(newps))
f = open('polygon.svg', 'a')
f.write('</svg>\n')
f.close()

print("done")

#print(points)
#print(newps)
