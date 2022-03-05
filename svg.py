"""svg writing"""

import shape
import forms
import geom


def write_svg_recursive(file, shapes):
    """write recursive form"""
    if not isinstance(shapes, list):
        single = shapes
#        if not isinstance(shapes, shape.Shape):
#            shap = shape.Shape(polygon.Polygon(shapes.get_points()))
        write_svg_shape(file, single)
        return
    for shap in shapes:
        write_svg_recursive(file, shap)


def write_svg_shape(file, single):
    """write shape"""
    app = single.appearance
    if isinstance(single.base, geom.Rect):
        r = single.base
        x = single.position.x - r.width / 2
        y = single.position.y - r.height / 2
        file.write(f'<rect x="{x}" y="{y}" '
                   f'height="{r.height}" width="{r.width}" '
                   f'style="opacity:{app.opacity};'
                   f'fill:{app.colour};stroke:{app.stroke};'
                   f'stroke-width:{app.stroke_width}" />\n')
        return
    if isinstance(single.base, geom.Circle):
        x = single.position.x
        y = single.position.y
        r = single.base.r
        file.write(f'<circle cx="{x}" cy="{y}" r="{r}" '
                   f'style="opacity:{app.opacity};'
                   f'fill:{app.colour};stroke:{app.stroke};'
                   f'stroke-width:{app.stroke_width}" />\n')
        return
    file.write('<polygon\n')
    file.write('points="')
    for p in single.get_rendering_points():
        file.write(f'{p.x},{p.y} ')
    file.write('"\n')
    file.write(
        f'style="opacity:{app.opacity};'
        f'fill:{app.colour};stroke:{app.stroke};'
        f'stroke-width:{app.stroke_width};stroke-linejoin:round" />\n')


def write_form(file, config):
    """write a form"""
    name = config.get('name')
    if name is None:
        return
    print(f"getting form {name}")
    sss = forms.get(name)
    if sss is not None:
        write_svg_recursive(file, sss)


def write(fname, height, width, config):
    bg = config.get("background", "white")
    shapes = config.get("shapes", [])
    with open(fname, 'w', encoding="utf-8") as file:
        file.write(
            f'<svg style="background-color:{bg}" '
            f'viewBox="0 0 2800 1800" '
            f'height="{height}" width="{width}" '
            f'xmlns="http://www.w3.org/2000/svg">\n')
        for fn in shapes:
            write_form(file, fn)
        file.write('</svg>\n')
