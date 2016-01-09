#!/usr/bin/env python

from ssbp import app
from ssbp.static_contents import make_views

if __name__ == '__main__':
    make_views()
    app.run(debug=True)
