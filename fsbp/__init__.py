
from __future__ import absolute_import

import os

from flask import Flask
from flask_assets import Environment, Bundle

# load user settings
import traceback

version = '0.1'

user_settings = {}
static_folder = os.path.join(os.getcwd(), 'contents/themes/precise/static')
template_folder = os.path.join(os.getcwd(), 'contents/themes/precise/templates')
template_config_path = os.path.join(os.getcwd(), 'contents/themes/precise/config.yml')

try:
    import settings

    for setting_key in dir(settings):
        if setting_key[0:2] == '__':
            continue
        if setting_key.isupper():
            user_settings[setting_key] = getattr(settings, setting_key)


    static_folder = os.path.join(os.getcwd(), 'contents/themes/{0}/static'.format(user_settings.get('THEME', 'precise')))
    template_folder = os.path.join(os.getcwd(), 'contents/themes/{0}/templates'.format(user_settings.get('THEME', 'precise')))
    template_config_path = os.path.join(os.getcwd(), 'contents/themes/{0}/config.yml'.format(user_settings.get('THEME', 'precise')))

except Exception as e:
    # print('unable to read user settings')
    # print(e)
    # traceback.print_exc()
    pass

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
assets = Environment(app)

import fsbp.settings
app.config.update(user_settings)


import fsbp.views

# load theme

if os.path.exists(template_config_path):
    import yaml
    with open(template_config_path) as f:
        theme_config = yaml.load(f, Loader=yaml.FullLoader)

    js = Bundle(
            *(theme_config.get('js', [])),
            filters='rjsmin', output='js/build.js'
            )

    css = Bundle(
            *(theme_config.get('css', [])),
            output='css/build.css'
            )

    assets.register('js_all', js)
    assets.register('css_all', css)
