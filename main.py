import form
import json
import default
import sys
import getopt
import svg


def readConfig(fname):
    print("reading config")
    f = open(fname, 'r')
    # json to dictionary
    data = json.load(f)
    f.close()
    print("init defaults")
    d = data.get('defaults')
    if d is not None:
        default.read(d)
    return data


def run(data, fname):
    print("initializing form table")
    form.initFormTable()
    print("generate forms")
    forms = data.get('forms')
    if forms is not None:
        for fd in forms:
            form.generateForm(fd)
    print("write output")
    op = data.get('output')
    if op is not None:
        svg.write(fname, 900, 1400, op, form.formTable)


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
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
    data = readConfig(inputfile)
    run(data, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])
