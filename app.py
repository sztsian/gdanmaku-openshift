#!/usr/bin/env python2
# -*- coding:utf-8 -*-
import os

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

from gdanmaku import main

if __name__ == "__main__":
    main()


# vim: ts=4 sw=4 sts=4 expandtab
