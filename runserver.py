#!/usr/bin/env python

from fsbp import app
from fsbp.static_contents import make_views

if __name__ == '__main__':
    make_views()
    app.run(debug=True)
