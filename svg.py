"""svg writing"""

import shape
import forms
import geom


def write_svg_feshadow(file, id):
    file.write(f'<filter id="{id}">'
               '<feGaussianBlur in="SourceAlpha" stdDeviation="3" />'
               '<feOffset dx="2" dy="4" />'
               '<feMerge>'
               '<feMergeNode />'
               '<feMergeNode in="SourceGraphic" />'
               '</feMerge>'
               '</filter>')


def write_svg_feblur(file, id):
    file.write(f'<filter id="{id}">'
               '<feGaussianBlur in="SourceGraphic" stdDeviation="5" />'
               '</filter>')


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


SHAPE_COUNT = 0


def write_svg_shape(file, single):
    """write shape"""
    if isinstance(single, shape.List):
        for b in single.shapes:
            write_svg_recursive(file, b)
        return
    app = single.appearance
    if app.shadow:
        write_svg_feshadow(file, f'shadow_n{SHAPE_COUNT}')
    if app.blur:
        write_svg_feblur(file, f'blur_n{SHAPE_COUNT}')
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
                   f'stroke-width:{app.stroke_width}"')
        if app.shadow:
            file.write(f' filter="url(#shadow_n{SHAPE_COUNT})"')
        if app.blur:
            file.write(f' filter="url(#blur_n{SHAPE_COUNT})"')
        file.write(' />\n')
        return
    file.write('<polygon\n')
    file.write('points="')
    for p in single.get_rendering_points():
        file.write(f'{p.x},{p.y} ')
    file.write('"\n')
    file.write(
        f'style="opacity:{app.opacity};'
        f'fill:{app.colour};stroke:{app.stroke};'
        f'stroke-width:{app.stroke_width};stroke-linejoin:round"')
    if app.shadow:
        file.write(f' filter="url(#shadow_n{SHAPE_COUNT})"')
    if app.blur:
        file.write(f' filter="url(#blur_n{SHAPE_COUNT})"')
    file.write(' />\n')


def write_svg_image(file, img, w, h, bg):
    """write image"""
    file.write(f'<mask id="{img.name}">'
               f'<rect x="0" y="0" width="2800" height="1800" fill="white" />\n')
    for d in img.paths:
        file.write(f'<path d="{d}" fill="black" />\n')
    file.write('</mask>\n')
    file.write(f'<rect x="0" y="0" '
               f'height="{h}" width="{w}" '
               f'fill="{bg}" mask="url(#{img.name})" />\n')
    return


def write_form(file, config, w, h, bg):
    """write a form"""
    name = config.get('name')
    if name is None:
        return
    print(f"getting form {name}")
    sss = forms.get(name)
    if sss is not None:
        write_svg_recursive(file, sss)
    else:
        write_image(file, name, w, h, bg)


def write_image(file, name, w, h, bg):
    """write an image"""
#    name = config.get('name')
#    if name is None:
#        return
    print(f"getting image {name}")
    sss = forms.get_image(name)
    if sss is not None:
        write_svg_image(file, sss, w, h, bg)


def write(fname, height, width, wbh, wbw, config):
    bg = config.get("background", "white")
    shapes = config.get("shapes", [])
    images = config.get("images", [])
    with open(fname, 'w', encoding="utf-8") as file:
        file.write(
            f'<svg style="background-color:{bg}" '
            f'viewBox="0 0 {wbw} {wbh}" '
            f'height="{height}" width="{width}" '
            f'xmlns="http://www.w3.org/2000/svg">\n')
        for fn in shapes:
            write_form(file, fn, width, height, bg)
#        for img in images:
#            write_image(file, img, bg)
        file.write('</svg>\n')
