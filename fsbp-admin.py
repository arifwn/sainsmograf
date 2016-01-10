#!/usr/bin/env python

from __future__ import absolute_import

import os
import shutil
import fsbp

if __name__ == '__main__':
    basedir = os.path.dirname(fsbp.__file__)
    sourcedir = os.path.join(basedir, 'data', 'project_structure')
    targetdir = os.path.join(os.getcwd(), 'contents')
    shutil.copytree(sourcedir, targetdir)
    shutil.copy2(os.path.join(basedir, 'bin', 'static.py'), os.path.join(os.getcwd(), 'static.py'))
    shutil.copy2(os.path.join(basedir, 'data', 'settings.py'), os.path.join(os.getcwd(), 'settings.py'))

    distdir = os.path.join(os.getcwd(), 'dist')
    if not os.path.exists(distdir):
        os.makedirs(distdir)
