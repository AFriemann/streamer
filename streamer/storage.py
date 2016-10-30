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

    if os.path.isfile(abspath):
        with open(abspath, 'r') as s:
            return { k: StorageEntry(**v) for k,v in yaml.safe_load(s).items() }

    return {}

def store(series, season, episode):
    abspath = os.path.expanduser(path or '~/.local/share/streamer/storage.yaml')

    storage = {}

    if os.path.isfile(abspath):
        with open(abspath, 'r') as s:
            storage = yaml.safe_load(s)

    storage.update(
        {
            series: {
                'season': season,
                'episode': episode,
            }
        }
    )

    with open(abspath, 'w') as s:
        s.write(yaml.safe_dump(storage, default_flow_style=False))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
