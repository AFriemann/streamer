# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os

try:
    import ruamel.yaml as yaml
except ImportError:
    import yaml

path = None

default = {
    'format': 'simple',
}

def read():
    abspath = os.path.expanduser(path or '~/.config/streamer/config.yaml')

    if os.path.isfile(abspath):
        with open(abspath, 'r') as s:
            default.update(yaml.safe_load(s))

    return default

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
