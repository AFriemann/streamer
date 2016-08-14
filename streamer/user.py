#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import collections, itertools
import tabulate as t

try:
    basestring
except NameError:
    basestring = str

def choose_one_of(lst):
    enumerated_lst = list(map(lambda i, x: (i,) + x, range(1, len(lst) + 1), lst))

    print(t.tabulate(enumerated_lst))

    allowed_values = list(range(1, len(lst) + 1))

    number = None
    while number not in allowed_values:
        try:
            number = int(input('choose: '))
            assert number in allowed_values
        except (AssertionError, ValueError): print('must be one of %s' % allowed_values)

    return lst[number - 1]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
