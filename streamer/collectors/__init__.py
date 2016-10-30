#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import abc

class Collector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def search(self, series):
        pass

    @abc.abstractmethod
    def seasons(self, series):
        pass

    @abc.abstractmethod
    def episodes(self, series, season):
        pass

    @abc.abstractmethod
    def providers(self, series, season, episode, whitelist, blacklist):
        pass

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
