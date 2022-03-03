"""svg writing"""

import shape
import forms


def write_svg_recursive(file, shapes):
    """write recursive form"""
    if not isinstance(shapes, list):
        single = shapes
        if not isinstance(shapes, shape.Shape):
            shap = shape.Shape()
            shap.points = shapes.toPolygon()
        write_svg_shape(file, single)
        return
    for shap in shapes:
        write_svg_recursive(file, shap)


def write_svg_shape(file, single):
    """write shape"""
    if isinstance(single, shape.Rect):
        file.write(f'<rect x="{single.x}" y="{single.y}" '
                   f'height="{single.height}" width="{single.width}" ')
        sw = 0
        if single.stroke != 'none':
            sw = 1
        file.write(
            f'style="opacity:{single.opacity};'
            f'fill:{single.colour};stroke:{single.stroke};stroke-width:{sw}" />\n')
        return
    file.write('<polygon\n')
    file.write('points="')
    for p in single.points:
        file.write(f'{p.x},{p.y} ')
    file.write('"\n')
    sw = 0
    if single.stroke != 'none':
        sw = 1
    file.write(
        f'style="opacity:{single.opacity};'
        f'fill:{single.colour};stroke:{single.stroke};stroke-width:{sw}" />\n')


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
            f'viewBox="-200 -200 1800 1300" '
            f'height="{height}" width="{width}" '
            f'xmlns="http://www.w3.org/2000/svg">\n')
        for fn in shapes:
            write_form(file, fn)
        file.write('</svg>\n')
