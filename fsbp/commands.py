
from __future__ import absolute_import

import argparse

import fsbp

parser = argparse.ArgumentParser(description='Flask Static Blogging Platform v{0}'.format(fsbp.version))
parser.add_argument('command', metavar='COMMAND', nargs='*', help='command to run (generate, runserver, add, test)')

args = parser.parse_args()


def run():
    if args.command[0] == 'runserver':
        from fsbp import app
        from fsbp.static_contents import make_views
        make_views()
        app.run(debug=False)


    if args.command[0] == 'generate':        
        from flask_frozen import Freezer
        from fsbp import app
        from fsbp.static_contents import make_views

        make_views()
        freezer = Freezer(app)
        freezer.freeze()

    if args.command[0] == 'add':
        from fsbp.utils import create_content

        title = args.command[2]
        slug = None
        if len(args.command) >= 4:
            slug = args.command[3]

        if args.command[1] == 'page':
            create_content('page', title, slug)
        if args.command[1] == 'post':
            create_content('post', title, slug)

