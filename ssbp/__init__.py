
from __future__ import absolute_import

import os

from flask import Flask
from flask.ext.assets import Environment, Bundle

# load user settings
import traceback

user_settings = {}
static_folder = os.path.join(os.getcwd(), 'contents/themes/precise/static')
template_folder = os.path.join(os.getcwd(), 'contents/themes/precise/templates')

try:
    import settings

    for setting_key in dir(settings):
        if setting_key[0:2] == '__':
            continue
        if setting_key.isupper():
            user_settings[setting_key] = getattr(settings, setting_key)


    static_folder = os.path.join(os.getcwd(), 'contents/themes/{0}/static'.format(user_settings.get('THEME', 'precise')))
    template_folder = os.path.join(os.getcwd(), 'contents/themes/{0}/templates'.format(user_settings.get('THEME', 'precise')))

except Exception, e:
    print('unable to read user settings')
    print(e)
    traceback.print_exc()

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
assets = Environment(app)

import ssbp.settings
app.config.update(user_settings)


import ssbp.views

# load theme

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
