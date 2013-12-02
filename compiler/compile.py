#! /usr/bin/env python
'''
compiler from svg and existing html (optional) to an amazing impress.js deck

Usage:
    compile.py [-o output] <svg> [<html>]
    compile.py (-h | --help)

Options:
    -h --help               Show help screen
    -o output               Output html file, if not given then print to stdout
    svg                     The svg file as the background and trace
    html                    An existing html, if given, necessary content will be appended to it
'''

from bs4 import BeautifulSoup as bs
from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__)
    # Here I only cache the svg in html file, waiting for js to deal with it
    with open(args['<svg>']) as f:
        svg = bs(f.read()).svg
        svg['class'] = 'cache'
        svg['style'] = 'display: none'

    html_file = args['<html>'] if args['<html>'] else 'template.html'
    with open(html_file) as f:
        doc = bs(f.read())

    exists = doc.select('svg#cache')
    if len(exists) > 0:
        exists.extract()
    doc.body.insert(0, svg)

    if args['-o']:
        with open(args['-o'], 'w') as f:
            f.write(doc.prettify())
    else:
        print str(doc)
