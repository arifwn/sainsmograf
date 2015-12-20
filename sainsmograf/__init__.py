
from flask import Flask
from flask.ext.assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)

import sainsmograf.settings
import sainsmograf.views

js = Bundle(
            'js/jquery-2.1.4.min.js',
            'js/moment.min.js',
            'js/parallax.min.js',
            'js/main.js',
            filters='rjsmin', output='js/build.js'
            )

css = Bundle(
            'css/font-awesome.min.css',
            'css/solarized-dark.css',
            'css/style.css',
            output='css/build.css'
            )

assets.register('js_all', js)
assets.register('css_all', css)
