# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import tabulate

table_formats = tabulate.tabulate_formats

table_format = None

def print_table(lst):
    print(tabulate.tabulate(lst, tablefmt=table_format or 'simple'))

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
