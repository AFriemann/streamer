#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import logging, base64, re

try: import urllib.parse as urlparse
except ImportError: import urlparse

import requests
from lxml import html

from streamer import web, user
from streamer.collectors import Collector

logger = logging.getLogger(__name__)

class watchseries(Collector):
    def __init__(self):
        self.root    = 'http://watch-series.to'
        self.session = requests.session()

        self.regex = re.compile(r'http(s)?://(the-)?watch-series.to')

    def assert_match(self, link):
        if web.absolute(link):
            assert self.matches(link), 'this link does not belong here: {}'.format(link)

    def matches(self, link):
        return self.regex.match(link)

    def get(self, link):
        try:
            response = self.session.get(link)
        except requests.exceptions.ConnectionError as e:
            raise Exception('failed to request {0} due to connection error: {1}'.format(link, repr(e)))

        assert response.status_code == 200, 'failed to request {0} with status_code {1}'.format(link, response.status_code)

        response.encoding = 'utf-8'

        return response

    def search(self, season):
        result = self.get(web.urljoin(self.root, 'search', season))

        tree = html.fromstring(result.text)

        for a in tree.xpath("//a[contains(@href,'/serie/')]"):
            path = a.xpath("@href")[0]
            name = a.xpath("normalize-space()")

            absolute = path if web.absolute(path) else web.urljoin(self.root, path)

            yield str(name).strip(), str(absolute).strip()

    def seasons(self, series):
        _, series_link = user.choose_one_of(list(self.search(series)), enumerate=True)

        self.assert_match(series_link)

        result = self.get(web.urljoin(series_link, 'sab'))

        tree = html.fromstring(result.text)

        for a in tree.xpath("//div[contains(@itemprop, 'season')]//a[contains(@href, '/season-')]"):
            path   = str(a.xpath("@href")[0]).strip()
            name   = a.xpath("normalize-space()")
            number = int(name.split()[1])

            absolute = path if web.absolute(path) else web.urljoin(self.root, path)

            yield number, absolute

    def episodes(self, series, season):
        seasons = sorted(list(self.seasons(series)))

        assert len(seasons) >= season, 'season {} could not be found'.format(season)

        _, season_link = seasons[season - 1] if season > 0 else user.choose_one_of(seasons)

        if not web.absolute(season_link):
            season_link = web.urljoin(self.root, season_link)

        self.assert_match(season_link)

        result = self.get(season_link)

        tree = html.fromstring(result.text)

        for li in tree.xpath("//li[contains(@itemprop, 'episode')]"):
            number = int(li.xpath("meta[contains(@itemprop, 'episodenumber')]/@content")[0])
            a      = li.xpath('a')[0]
            path   = str(a.xpath("@href")[0]).strip()
            name   = str(' '.join(a.xpath("span[contains(@itemprop, 'name')]/text()")[0].split()[2:])).strip()

            absolute = path if web.absolute(path) else web.urljoin(self.root, path)

            yield number, name, absolute

    def providers(self, series, season, episode, whitelist, blacklist):
        episodes = sorted(self.episodes(series, season))

        assert len(episodes) >= episode, 'episode {} could not be found'.format(episode)

        _, _, episode_link = episodes[episode - 1] if episode > 0 else user.choose_one_of(episodes)

        self.assert_match(episode_link)

        result = self.get(episode_link)

        tree = html.fromstring(result.text)

        for a in tree.xpath("//tr[contains(@class, 'download_link_')]/td[2]/a"):
            provider = str(a.xpath("@title")[0]).strip()

            if provider == "Sponsored" or provider in blacklist: continue
            elif len(whitelist) > 0 and provider not in whitelist: continue

            path = str(a.xpath("@href")[0]).strip()

            absolute = path if web.absolute(path) else web.urljoin(self.root, path)

            yield provider, self._resolve_provider_(absolute)

    def _resolve_provider_(self, link):
        self.assert_match(link)

        return base64.b64decode(link.split('?r=')[1]).decode()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
