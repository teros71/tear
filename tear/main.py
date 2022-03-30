"""Main for generating art"""

import logging
import os
import json
import sys
import getopt
from tear import default, form, pg, goldenratio, svg
from tear.model import store

log = logging.getLogger(__name__)


def read_config(fname):
    """Read json config"""
    log.info("reading config")
    with open(fname, 'r', encoding="utf-8") as conf_file:
        # json to dictionary
        data = json.load(conf_file)
    log.info("init defaults")
    defs = data.get('defaults')
    if defs is not None:
        default.read(defs)
    play = data.get('playground')
    if play is not None:
        pg.WIDTH = play.get('w', 1000)
        pg.HEIGHT = play.get('h', 1000)
        pg.CENTER_X = pg.WIDTH / 2
        pg.CENTER_Y = pg.HEIGHT / 2
        pg.GR_X1 = pg.WIDTH / goldenratio.VALUE
        pg.GR_Y1 = pg.HEIGHT / goldenratio.VALUE
        pg.GR_X0 = pg.WIDTH - pg.GR_X1
        pg.GR_Y0 = pg.HEIGHT - pg.GR_Y1
    return data


def process(data, fname):
    """Process the input data and generate output"""
    log.info("initializing form table")
    store.init()
    log.info("make templates")
    temp_data = data.get('templates')
    if temp_data is not None:
        if not isinstance(temp_data, list):
            raise ValueError("invalid template data")
        log.info(f"{len(temp_data)} templates")
        for temp in temp_data:
            name = temp.get('name')
            store.add_template(name, temp)
    log.info("generate forms")
    form_data = data.get('forms')
    if form_data is not None:
        for fd in form_data:
            form.generate_form(fd)
    log.info("write output")
    op = data.get('output')
    if op is None:
        log.warning("no output defined!")
        return
    if not isinstance(op, dict):
        raise ValueError("invalid output configuration")
    svg.write(fname, pg.HEIGHT, pg.WIDTH, pg.HEIGHT, pg.WIDTH, op)


def main(argv):
    """main"""
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
    inputfile = ''
    outputfile = ''
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <configfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    log.info('Input file: %s', inputfile)
    log.info('Output file: %s', outputfile)
    data = read_config(inputfile)
    process(data, outputfile)
