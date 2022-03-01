import shape


def writeSVGRecursive(f, forms):
    if type(forms) is not list:
        s = forms
        if type(forms) is not shape.Shape:
            s = shape.Shape()
            s.points = forms.toPolygon()
        writeSVGShape(f, s)
        return
    for form in forms:
        writeSVGRecursive(f, form)


def writeSVGShape(f, s):
    f.write('<polygon\n')
    f.write('points="')
    for p in s.points:
        f.write('{0},{1} '.format(p.x, p.y))
    f.write('"\n')
    sw = 0
    if s.stroke != 'none':
        sw = 1
    f.write(
        'style="opacity:{0};fill:{1};stroke:{2};stroke-width:{3}" />\n'.format(s.opacity, s.colour, s.stroke, sw))


def writeForm(f, fn, shapeTable):
    name = fn.get('name')
    if name is None:
        return
    print("getting form {0}".format(name))
    sss = shapeTable.get(name)
    if sss is not None:
        writeSVGRecursive(f, sss)


def write(fname, height, width, out, shapeTable):
    bg = out.get("background", "white")
    forms = out.get("shapes", [])
    f = open(fname, 'w')
    f.write(
        '<svg style="background-color:{0}" viewBox="-200 -200 1800 1300" height="{1}" width="{2}" xmlns="http://www.w3.org/2000/svg">\n'.format(bg, height, width))
    for fn in forms:
        writeForm(f, fn, shapeTable)
    f.write('</svg>\n')
    f.close()
