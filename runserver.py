#!/usr/bin/env python

from sainsmograf import app
from sainsmograf.static_contents import make_views
import settings

if __name__ == '__main__':
    make_views()
    app.run(debug=True)
