#!/usr/bin/env python

from flask_frozen import Freezer

from fsbp import app
from fsbp.static_contents import make_views


if __name__ == '__main__':
    make_views()
    freezer = Freezer(app)
    freezer.freeze()
