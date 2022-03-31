"""svg writing"""

import logging
from tear.model import shape
from tear.geometry import geom, path
from tear.model import store

log = logging.getLogger(__name__)


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


def write_svg_clip(file, id, shap):
    file.write(f'<clipPath id="{id}">')

    def write_one_clip(s):
        if isinstance(s, shape.List):
            for ss in s:
                write_one_clip(ss)
            return
        if isinstance(s.g, geom.Rect):
            write_svg_rect(file, s.g)
        elif isinstance(s.g, geom.Circle):
            write_svg_circle(file, s.g)
        elif isinstance(s.g, geom.Ellipse):
            write_svg_ellipse(file, s)
        else:
            write_svg_polygon(file, s.g)
        file.write(' />\n')
    write_one_clip(shap)
    file.write('</clipPath>')
#      <defs>
#      </defs>


def write_svg_mask(file, id, shap):
    """write image"""
    file.write(f'<mask id="{id}">')
    file.write(
        f'<rect x="0" y="0" width="100%" height="100%" fill="white" />\n')
    write_svg_geom(file, shap)
    file.write('fill="black" />')
    file.write('</mask>\n')
    return


def write_svg_recursive(file, shapes):
    """write recursive form"""
    if not isinstance(shapes, list):
        #print(shapes)
        single = shapes
#        if not isinstance(shapes, shape.Shape):
#            shap = shape.Shape(polygon.Polygon(shapes.get_points()))
        write_svg_shape(file, single)
        return
    log.debug("recursive list shape")
    for shap in shapes:
        write_svg_recursive(file, shap)


SHAPE_COUNT = 0


def write_svg_rect(file, g):
    x = g.position.x - g.width / 2
    y = g.position.y - g.height / 2
    file.write(f'<rect x="{x}" y="{y}" '
               f'height="{g.height}" width="{g.width}" ')


def write_svg_circle(file, g):
    x = g.position.x
    y = g.position.y
    file.write(f'<circle cx="{x}" cy="{y}" r="{g.radius}" ')


def write_svg_ellipse(file, e):
    g = e.g
    x = g.position.x
    y = g.position.y
    rx = g.rx
    ry = g.ry
    file.write(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" ')
    if e.angle != 0:
        a = e.angle
        file.write(f'transform="rotate({a} {x} {y})" ')


def write_svg_polygon(file, poly):
    file.write('<polygon\n')
    file.write('points="')
    for p in poly.get_points():
        file.write(f'{p.x},{p.y} ')
    file.write('"\n')


def write_svg_path(file, g):
    """Write path"""

    def write_cubic(segs):
        first = True
        for s in segs:
            if first:
                file.write(
                    f'C {s.c0.x} {s.c0.y} {s.c1.x} {s.c1.y} {s.p1.x} {s.p1.y} ')
                first = False
            else:
                file.write(f'S {s.c1.x} {s.c1.y} {s.p1.x} {s.p1.y} ')

    def write_quadratic(segs):
        first = True
        for s in segs:
            if first:
                file.write(
                    f'Q {s.cp.x} {s.cp.y} {s.p1.x} {s.p1.y} ')
                first = False
            else:
                file.write(f'T {s.p1.x} {s.p1.y} ')

    log.debug("path element:path={%s}", g)
    p = g.startpoint
    file.write(f'<path d="M {p.x} {p.y} ')
    if isinstance(g.segments[0], geom.CubicCurve):
        write_cubic(g.segments)
    else:
        write_quadratic(g.segments)
    file.write('" ')


def write_svg_path_debug(file, path):
    def wp(p, c):
        file.write(
            f'<circle cx="{p.x}" cy="{p.y}" r="10" fill="{c}" opacity="0.5"/>')
    for s in path.segments:
        if isinstance(s, geom.CubicCurve):
            wp(s.p0, "black")
            wp(s.p1, "white")
            wp(s.c0, "green")
            wp(s.c1, "blue")
        else:
            wp(s.p0, "black")
            wp(s.p1, "white")
            wp(s.cp, "green")


def write_svg_style(file, app):
    file.write(
        f'style="opacity:{app.opacity};'
        f'fill:{app.colour};stroke:{app.stroke};'
        f'stroke-width:{app.stroke_width};stroke-linejoin:round"')


def write_svg_geom(file, shap):
    if isinstance(shap.g, geom.Rect):
        write_svg_rect(file, shap.g)
    elif isinstance(shap.g, geom.Circle):
        write_svg_circle(file, shap.g)
    elif isinstance(shap.g, geom.Ellipse):
        write_svg_ellipse(file, shap)
    elif isinstance(shap.g, geom.Polygon):
        write_svg_polygon(file, shap.g)
    elif isinstance(shap.g, path.Path):
        write_svg_path(file, shap.g)


def write_svg_shape(file, single):
    """write shape"""
    global SHAPE_COUNT
    SHAPE_COUNT += 1
    if isinstance(single, shape.List):
        if single.appearance.clip is not None:
            file.write(f'<g clip-path="url(#{single.appearance.clip})">')
        else:
            file.write('<g>')
        for b in single.shapes:
            write_svg_recursive(file, b)
        file.write('</g>')
        return
    app = single.appearance
    if app.shadow:
        write_svg_feshadow(file, f'shadow_n{SHAPE_COUNT}')
    if app.blur:
        write_svg_feblur(file, f'blur_n{SHAPE_COUNT}')
    write_svg_geom(file, single)
    write_svg_style(file, app)
    if app.shadow:
        file.write(f' filter="url(#shadow_n{SHAPE_COUNT})"')
    if app.blur:
        file.write(f' filter="url(#blur_n{SHAPE_COUNT})"')
    if app.mask is not None:
        file.write(f' mask="url(#{app.mask})"')
    file.write(' />\n')
    #if isinstance(single.base, path.Path):
    #    write_svg_path_debug(file, single.base)


def write_svg_image(file, img, w, h, bg):
    """write image"""
    file.write(f'<mask id="{img.name}">'
               f'<rect x="0" y="0" width="2800" height="2000" fill="white" />\n')
    for d in img.paths:
        file.write(f'<path d="{d}" fill="black" />\n')
    file.write('</mask>\n')
    file.write(f'<rect x="0" y="0" '
               f'height="{h}" width="{w}" '
               f'fill="{bg}" mask="url(#{img.name})" />\n')
    return


def write_form(file, config, w, h, bg):
    """write a form"""
    if isinstance(config, dict):
        name = config.get('name')
        if name is None:
            return
    elif isinstance(config, str):
        name = config
    log.info(f"getting shape {name}")
    sss = store.get_shape(name)
    if sss is not None:
        #        print(sss)
        write_svg_recursive(file, sss)
#    else:
#        write_image(file, name, w, h, bg)


#def write_image(file, name, w, h, bg):
#    """write an image"""
#    print(f"getting image {name}")
#    sss = forms.get_image(name)
#    if sss is not None:
#        write_svg_image(file, sss, w, h, bg)


def write_clips(file):
    file.write('<defs>')
    log.info(f"clips {store.get_clips()}")
    for clipid, name in store.get_clips():
        clip = store.get_shape(name)
        write_svg_clip(file, clipid, clip)
    for maskid, name in store.get_masks():
        mask = store.get_shape(name)
        write_svg_mask(file, maskid, mask)
    file.write('</defs>')


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
        write_clips(file)
        for fn in shapes:
            write_form(file, fn, width, height, bg)
#        for img in images:
#            write_image(file, img, bg)
        file.write('</svg>\n')
