#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import abc

class Collector:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def search(self, series):
        pass

    @abc.abstractmethod
    def seasons(self, link):
        pass

    @abc.abstractmethod
    def episodes(self, link):
        pass

    @abc.abstractmethod
    def providers(self, link):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
