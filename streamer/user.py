#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import collections, itertools, sys
import tabulate as t

try:
    basestring
except NameError:
    basestring = str

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def choose_one_of(lst, enumerate=False):
    if not enumerate: enumerated_lst = lst
    else: enumerated_lst = list(map(lambda i, x: (i,) + x, range(1, len(lst) + 1), lst))

    assert len(enumerated_lst) > 0, 'received empty list.'
    assert type(enumerated_lst[0][0]) is int, 'first element in sublist must be an integer.'

    sys.stderr.write(t.tabulate(enumerated_lst) + '\n')
    sys.stderr.flush()

    if len(enumerated_lst) == 1: return lst[0]

    allowed_values = [ content[0] for content in enumerated_lst ]

    number = None
    while number not in allowed_values:
        try:
            sys.stderr.write('choose: ')
            number = int(input())
            sys.stderr.flush()
            assert number in allowed_values
        except (AssertionError, ValueError):
            sys.stderr.write('must be one of %s\n' % allowed_values)
            sys.stderr.flush()

    result = [ value for value in enumerated_lst if value[0] == number ]

    assert len(result) == 1, 'found several values with the same number: %s' % result

    return result[0][1:]

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
