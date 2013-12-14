#! /usr/bin/env python
'''
compiler from svg and existing html (optional) to an amazing impress.js deck (powered by inkpress)

Usage:
    compile.py [-t template] [-o output] [-b svg] [<input>]
    compile.py (-h | --help)

Options:
    -h --help               Show help screen
    -o output               Output html file, if not given then print to stdout
    -t template             Template file to be used
    -b svg                  The svg file as the background and trace
    input                   Can be html or markdown, if not given template
                            will be used
'''

import os
import sys


curdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(curdir, 'lib'))

from bs4 import BeautifulSoup as bs
from docopt import docopt
import markdown2


default_template = os.path.abspath(os.path.join(curdir, 'template.html'))


def insert_svg(doc, svg):
    svg['class'] = 'cache'
    svg['style'] = 'display: none'

    exists = doc.select('svg.cache')
    if len(exists) > 0:
        exists.extract()
    doc.body.insert(0, svg)


def process_md(md_file, template_text):
    templ = bs(template_text)
    plain_doc = bs(markdown2.main(md_file))

    container = templ.select('#impress')[0]

    def new_step(i):
        new = bs('<div></div>')
        new.div['class'] = 'step'
        new.div['id'] = i
        return new.div

    i = 0
    current = new_step(i)
    for node in plain_doc.body.children:
        if not hasattr(node, 'name'):
            continue
        elif node.name == 'hr':
            i += 1
            container.append(current)
            current = new_step(i)
        else:
            current.append(node)
    container.append(current)
    return templ


if __name__ == '__main__':
    args = docopt(__doc__)

    template = args['-t'] if args['-t'] else default_template
    in_file = args['<input>'] if args['<input>'] else template

    if in_file.endswith('.md') or in_file.endswith('.markdown'):
        with open(template) as f:
            doc = process_md(in_file, f.read())
    else:
        with open(in_file) as f:
            doc = bs(f.read())

    if args['-b']:
        # Here I only cache the svg in html file, waiting for js to deal with it
        with open(args['-b']) as f:
            svg = bs(f.read()).svg
        insert_svg(doc, svg)

    if args['-o']:
        with open(args['-o'], 'w') as f:
            f.write(doc.prettify())
    else:
        print str(doc)
