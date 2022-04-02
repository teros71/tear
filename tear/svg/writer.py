"""svg writing"""

import logging
from tear.model import shape
from tear.geometry import geom, path, image, text
from tear.model import store

log = logging.getLogger(__name__)

SHAPE_COUNT = 0


def write(fname, height, width, wbh, wbw, config):
    """Write svg file"""
    bg = config.get("background", "white")
    shapes = config.get("shapes", [])
#    images = config.get("images", [])
    with open(fname, 'w', encoding="utf-8") as file:
        file.write(
            f'<svg style="background-color:{bg}" '
            f'viewBox="0 0 {wbw} {wbh}" '
            f'height="{height}" width="{width}" '
            'xmlns="http://www.w3.org/2000/svg" '
            'xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        write_clips(file)
        for ss in shapes:
            sn, s = get_shape(ss)
            if s is None:
                log.warning("shape is not available;name=%s",
                            sn if sn else "-")
            else:
                log.info("writing shape;name=%s", sn)
                write_shape(file, s)
#        for img in images:
#            write_image(file, img, bg)
        file.write('</svg>\n')


def get_shape(config):
    """write a form"""
    if isinstance(config, dict):
        # old style dict with name
        name = config.get('name')
        if name is None:
            log.warning("shape name not available")
            return None, None
    elif isinstance(config, str):
        name = config
    else:
        log.error("unsupported config")
        return None, None
    return name, store.get_shape(name)


def write_shape(file, shap):
    """write shape"""
    global SHAPE_COUNT

    if isinstance(shap, shape.List):
        write_list(file, shap)
        return
    SHAPE_COUNT += 1
    app = shap.appearance
    if app.shadow:
        write_feshadow(file, f'shadow_n{SHAPE_COUNT}')
    if app.blur:
        write_feblur(file, f'blur_n{SHAPE_COUNT}')
    if write_geom(file, shap):
        return
    write_style(file, app)
    if app.shadow:
        file.write(f' filter="url(#shadow_n{SHAPE_COUNT})"')
    if app.blur:
        file.write(f' filter="url(#blur_n{SHAPE_COUNT})"')
    if app.mask is not None:
        file.write(f' mask="url(#{app.mask})"')
    file.write(' />\n')
#    if isinstance(shap.g, path.Path):
#        write_svg_path_debug(file, shap.g)


def write_list(file, lst):
    global SHAPE_COUNT
    SHAPE_COUNT += 1

    if lst.appearance.blur:
        write_feblur(file, f'blur_n{SHAPE_COUNT}')

    file.write('<g')
    if lst.appearance.clip is not None:
        file.write(f' clip-path="url(#{lst.appearance.clip})"')
    if lst.appearance.blur:
        file.write(f' filter="url(#blur_n{SHAPE_COUNT})"')
    file.write('>')
    for s in lst:
        write_shape(file, s)
    file.write('</g>')


# write geometry objects

def write_geom(file, shap):
    """Write geometry of shape"""
    if isinstance(shap.g, geom.Rect):
        write_rect(file, shap.g)
    elif isinstance(shap.g, geom.Circle):
        write_circle(file, shap.g)
    elif isinstance(shap.g, geom.Ellipse):
        write_ellipse(file, shap.g, shap.angle)
    elif isinstance(shap.g, geom.Polygon):
        write_polygon(file, shap.g)
    elif isinstance(shap.g, path.Path):
        write_path(file, shap.g)
    elif isinstance(shap.g, image.Image):
        write_image(file, shap.g)
    elif isinstance(shap.g, text.Text):
        write_text(file, shap)
        return True
    return False


def write_rect(file, g):
    """rect"""
    x = g.position.x - g.width / 2
    y = g.position.y - g.height / 2
    file.write(f'<rect x="{x}" y="{y}" '
               f'height="{g.height}" width="{g.width}" ')


def write_circle(file, g):
    """circle"""
    x = g.position.x
    y = g.position.y
    file.write(f'<circle cx="{x}" cy="{y}" r="{g.radius}" ')


def write_ellipse(file, g, angle):
    """ellipse"""
    x = g.position.x
    y = g.position.y
    rx = g.rx
    ry = g.ry
    file.write(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" ')
    if angle != 0:
        file.write(f'transform="rotate({angle} {x} {y})" ')


def write_polygon(file, poly):
    """polygon"""
    file.write('<polygon\n')
    file.write('points="')
    for p in poly.get_points():
        file.write(f'{p.x},{p.y} ')
    file.write('"\n')


def write_path(file, g):
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
    """debug path"""
    def wp(p, c):
        file.write(
            f'<circle cx="{p.x}" cy="{p.y}" r="10" fill="{c}" opacity="0.5"/>')
    for s in path.segments:
        if isinstance(s, geom.CubicCurve):
            wp(s.p0, "blue")
            wp(s.p1, "red")
            wp(s.c0, "green")
            wp(s.c1, "yellow")
        else:
            wp(s.p0, "blue")
            wp(s.p1, "red")
            wp(s.cp, "green")


def write_image(file, img):
    x = img.position.x - img.width / 2
    y = img.position.y - img.height / 2
    file.write(f'<image href="{img.path}" '
               f'x="{x}" y="{y}" '
               f'height="{img.height}" width="{img.width}" ')


def write_text(file, txt):
    x = txt.position.x
    y = txt.position.y
    file.write(f'<text x="{x}" y="{y}" text-anchor="middle" '
               f'font-size="{txt.g.size}px" ')
    write_style(file, txt.appearance)
    file.write('>')
    file.write(txt.g.text)
    file.write('</text>')


def write_style(file, app):
    """Style settings for object"""
    file.write(
        f'style="opacity:{app.opacity};'
        f'fill:{app.colour};stroke:{app.stroke};'
        f'stroke-width:{app.stroke_width};stroke-linejoin:round"')

# filters


def write_feshadow(file, id):
    file.write(f'<filter id="{id}">'
               '<feGaussianBlur in="SourceAlpha" stdDeviation="3" />'
               '<feOffset dx="2" dy="4" />'
               '<feMerge>'
               '<feMergeNode />'
               '<feMergeNode in="SourceGraphic" />'
               '</feMerge>'
               '</filter>')


def write_feblur(file, id):
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
            write_rect(file, s.g)
        elif isinstance(s.g, geom.Circle):
            write_circle(file, s.g)
        elif isinstance(s.g, geom.Ellipse):
            write_ellipse(file, s.g, s.angle)
        else:
            write_polygon(file, s.g)
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
    write_geom(file, shap)
    file.write('fill="black" />')
    file.write('</mask>\n')
    return


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
