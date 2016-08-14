#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import logging, base64

try: import urllib.parse as urlparse
except ImportError: import urlparse

import requests
from lxml import html

from . import Collector
from .. import web

logger = logging.getLogger(__name__)

class watchseries(Collector):
    def __init__(self):
        self.root    = 'http://watch-series.to'
        self.session = requests.session()

    def search(self, season):
        result = self.session.get(web.urljoin(self.root, 'search', season))

        tree = html.fromstring(result.text)

        for a in tree.xpath("//a[contains(@href,'/serie/')]"):
            relative = a.xpath("@href")[0]
            absolute = web.urljoin(self.root, relative)
            name     = a.xpath("normalize-space()")
            yield str(name), str(absolute)

    def seasons(self, link):
        assert link.startswith(self.root), 'this link does not belong here: %s' % link

        result = self.session.get(web.urljoin(link, 'sab'))

        tree = html.fromstring(result.text)

        for a in tree.xpath("//div[contains(@itemprop, 'season')]//a[contains(@href, '/season-')]"):
            absolute = a.xpath("@href")[0]
            name     = a.xpath("normalize-space()")
            number   = name.split()[1]

            yield str(number), str(absolute)

    def episodes(self, link):
        assert link.startswith(self.root), 'this link does not belong here: %s' % link

        result = self.session.get(link)

        tree = html.fromstring(result.text)

        for li in tree.xpath("//li[contains(@itemprop, 'episode')]"):
            number   = li.xpath("meta[contains(@itemprop, 'episodenumber')]/@content")[0]
            a        = li.xpath('a')[0]
            relative = a.xpath("@href")[0]
            absolute = web.urljoin(self.root, relative)
            name     = ' '.join(a.xpath("span[contains(@itemprop, 'name')]/text()")[0].split()[2:])

            yield int(number), str(name), str(absolute)

    def providers(self, link):
        assert link.startswith(self.root), 'this link does not belong here: %s' % link

        result = self.session.get(link)

        tree = html.fromstring(result.text)

        for a in tree.xpath("//tr[contains(@class, 'download_link_')]/td[2]/a"):
            provider = a.xpath("@title")[0]
            if provider == "Sponsored": continue

            relative = a.xpath("@href")[0]
            absolute = web.urljoin(self.root, relative)

            yield str(provider), str(self._resolve_provider_(absolute))

    def _resolve_provider_(self, link):
        assert link.startswith(self.root), 'this link does not belong here: %s' % link

        return base64.b64decode(link.split('?r=')[1]).decode()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
