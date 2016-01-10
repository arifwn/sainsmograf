
from __future__ import absolute_import

import os
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

        host = args.command[1] if len(args.command) > 1 else '127.0.0.1'
        port = int(args.command[2]) if len(args.command) > 2 else 5000

        contents_dir = app.config.get('STATIC_CONTENTS_DIR', 'contents')
        extra_dirs = [os.path.join(os.getcwd(), contents_dir, 'pages'), os.path.join(os.getcwd(), contents_dir, 'posts')]
        extra_files = extra_dirs[:]
        for extra_dir in extra_dirs:
            for dirname, dirs, files in os.walk(extra_dir):
                for filename in files:
                    filename = os.path.join(dirname, filename)
                    if os.path.isfile(filename):
                        extra_files.append(filename)

        app.debug = True
        app.run(host, port, extra_files=extra_files)

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
            filepath = create_content('page', title, slug)
        if args.command[1] == 'post':
            filepath = create_content('post', title, slug)

        print('{0} created at {1}'.format(args.command[1], filepath))

