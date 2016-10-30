#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

def urljoin(*args):
    """
    Joins given arguments into a url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).lstrip('/').rstrip('/'), args))

def relative(path):
    return path.startswith('/')

def absolute(path):
    return not relative(path) and path.startswith('http')

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
