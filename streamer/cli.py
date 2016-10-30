#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import importlib, sys, os, logging, pkgutil, click

from . import collectors, user, data, config

logger = logging.getLogger(__name__)

pass_collector   = click.make_pass_decorator(collectors.Collector)

valid_collectors = [ foo for _, foo, _ in pkgutil.iter_modules([os.path.dirname(collectors.__file__)]) ]
valid_formats    = data.table_formats

@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option('-c', '--cfg', type=click.Path(dir_okay=False))
@click.option('-p', '--collector', default='watchseries', type=click.Choice(valid_collectors))
@click.option('-f', '--format', type=click.Choice(valid_formats))
@click.option('-d', '--debug/--no-debug', default=False)
@click.pass_context
def main(ctx, cfg, collector, format, debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING)

    module  = importlib.import_module('.collectors.%s' % (collector), package=__package__)
    ctx.obj = getattr(module, collector)()

    config.path = cfg
    data.table_format = format or config.read().get('format')

@main.command()
@click.argument('series')
@pass_collector
def search(collector, series):
    try:
        results = list(collector.search(series))

        data.print_table(results)
    except AssertionError as e:
        logger.error(e)

@main.command()
@click.argument('series')
@pass_collector
def seasons(collector, series):
    try:
        name, link = user.choose_one_of(list(collector.search(series)), enumerate=True)

        results = collector.seasons(link)

        data.print_table(list(results))
    except AssertionError as e:
        logger.error(e)

@main.command()
@click.argument('series')
@click.argument('season', default=-1, type=int)
@pass_collector
def episodes(collector, series, season):
    try:
        series_name, series_link = user.choose_one_of(list(collector.search(series)), enumerate=True)

        seasons = sorted(list(collector.seasons(series_link)))
        assert len(seasons) >= season, 'season %s could not be found' % season
        season_number, season_link = seasons[season - 1] if season > 0 else user.choose_one_of(seasons)

        episodes = list(collector.episodes(season_link))

        data.print_table(sorted(episodes))
    except AssertionError as e:
        logger.error(e)

@main.command()
@click.option('--whitelist', '-w', multiple=True)
@click.option('--blacklist', '-b', multiple=True)
@click.argument('series')
@click.argument('season', default=-1, type=int)
@click.argument('episode', default=-1, type=int)
@pass_collector
def episode(collector, whitelist, blacklist, series, season, episode):
    try:
        cfg = config.read()

        whitelist = set(whitelist).union(set(cfg.get('whitelist') or []))
        blacklist = set(blacklist).union(set(cfg.get('blacklist') or []))

        series_name, series_link = user.choose_one_of(list(collector.search(series)), enumerate=True)

        seasons = sorted(list(collector.seasons(series_link)))
        assert len(seasons) >= season, 'season %s could not be found' % season
        season_number, season_link = seasons[season - 1] if season > 0 else user.choose_one_of(seasons)

        episodes = sorted(list(collector.episodes(season_link)))
        assert len(episodes) >= episode, 'episode %s could not be found' % episode
        episode_number, episode_name, episode_link = episodes[episode - 1] if episode > 0 else user.choose_one_of(episodes)

        providers = filter(lambda x: not blacklist or x[0] not in blacklist,
            filter(lambda x: not whitelist or x[0] in whitelist,
                collector.providers(episode_link)
            )
        )

        data.print_table(sorted(providers))
    except AssertionError as e:
        logger.error(e)

if __name__ == '__main__':
    exit(main())

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
