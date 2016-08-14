#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import importlib, sys, os, logging
import click, tabulate as t

from .collectors import Collector
from . import user

pass_collector = click.make_pass_decorator(Collector)

@click.group()
@click.option('-p', '--collector', default='watchseries')
@click.option('-d', '--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, collector, debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING)

    module = importlib.import_module('.collectors.%s' % (collector), package=__package__)
    ctx.obj = getattr(module, collector)()

@main.command()
@click.argument('series')
@pass_collector
def search(collector, series):
    results = list(collector.search(series))

    print(t.tabulate(results))

@main.command()
@click.argument('series')
@pass_collector
def seasons(collector, series):
    name, link = user.choose_one_of(list(collector.search(series)))

    results = collector.seasons(link)

    print(t.tabulate(list(results)))

@main.command()
@click.argument('series')
@click.argument('season', default=-1, type=int)
@pass_collector
def episodes(collector, series, season):
    series_name, series_link = user.choose_one_of(list(collector.search(series)))

    seasons = list(map(lambda x: x[1:], sorted(list(collector.seasons(series_link)))))
    season_link, = seasons[season - 1] if season > 0 else user.choose_one_of(seasons)

    episodes = list(collector.episodes(season_link))

    print(t.tabulate(sorted(episodes)))

@main.command()
@click.argument('series')
@click.argument('season', default=-1, type=int)
@click.argument('episode', default=-1, type=int)
@pass_collector
def episode(collector, series, season, episode):
    series_name, series_link = user.choose_one_of(list(collector.search(series)))

    seasons = list(map(lambda x: x[1:], sorted(list(collector.seasons(series_link)))))
    season_link, = seasons[season - 1] if season > 0 else user.choose_one_of(seasons)

    print(season_link)

    episodes = list(map(lambda x: x[1:], sorted(list(collector.episodes(season_link)))))
    episode_name, episode_link = episodes[episode - 1] if episode > 0 else user.choose_one_of(episodes)

    providers = collector.providers(episode_link)

    print(t.tabulate(sorted(providers)))

if __name__ == '__main__':
    exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
