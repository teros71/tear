"""Main for generating art"""

import json
import sys
import getopt
import svg
import default
import forms
import form
import pg
import goldenratio


def read_config(fname):
    """Read json config"""
    print("reading config")
    with open(fname, 'r', encoding="utf-8") as conf_file:
        # json to dictionary
        data = json.load(conf_file)
    print("init defaults")
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


def run(data, fname):
    """run the generation"""
    print("initializing form table")
    forms.init()
    print("generate forms")
    form_data = data.get('forms')
    if form_data is not None:
        for fd in form_data:
            form.generate_form(fd)
    print("write output")
    op = data.get('output')
    if op is not None:
        svg.write(fname, 1350, 900, pg.HEIGHT, pg.WIDTH, op)


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('main.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print('Input file is "', inputfile)
    print('Output file is "', outputfile)
    data = read_config(inputfile)
    run(data, outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
