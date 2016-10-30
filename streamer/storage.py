# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import os

from simple_model import Model, Attribute

try:
    import ruamel.yaml as yaml
except ImportError:
    import yaml

class StorageEntry(Model):
    season = Attribute(int)
    episode = Attribute(int)

path = None

def read():
    abspath = os.path.expanduser(path or '~/.local/share/streamer/storage.yaml')

    stored_series = []

    if os.path.isfile(abspath):
        with open(abspath, 'r') as s:
            return { k: StorageEntry(**v) for k,v in yaml.safe_load(s).items() }

    return {}

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
