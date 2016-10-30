#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: TODO
   :platform: Unix
   :synopsis: TODO.

.. moduleauthor:: Aljosha Friemann aljosha.friemann@gmail.com

"""

import importlib, sys, os, logging, pkgutil, click, time

from streamer import collectors, user, data, config, storage

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
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    if not debug: logging.getLogger('requests').setLevel(logging.WARNING)

    module  = importlib.import_module('.collectors.{}'.format(collector), package=__package__)
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
        results = collector.seasons(series)

        data.print_table(sorted(results))
    except AssertionError as e:
        logger.error(e)

@main.command()
@click.argument('series')
@click.argument('season', default=-1, type=int)
@pass_collector
def episodes(collector, series, season):
    try:
        episodes = collector.episodes(series, season)

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

        providers = sorted(collector.providers(series, season, episode, whitelist, blacklist))

        assert len(providers) > 0, 'no providers found with current settings'

        data.print_table(providers)
    except AssertionError as e:
        logger.error(e)

@main.group()
@click.option('-s', '--storage', type=click.Path(dir_okay=False))
def watch(storage):
    pass

@watch.command()
@click.option('--whitelist', '-w', multiple=True)
@click.option('--blacklist', '-b', multiple=True)
@click.argument('series')
@pass_collector
def next(collector, whitelist, blacklist, series):
    try:
        store = storage.read().get(series)
        assert store is not None, 'series {} not found in storage'.format(series)

        season = store.season
        episode = store.episode + 1

        logger.info('looking for s{0}e{1}'.format(season, episode))

        cfg = config.read()

        whitelist = set(whitelist).union(set(cfg.get('whitelist') or []))
        blacklist = set(blacklist).union(set(cfg.get('blacklist') or []))

        providers = sorted(collector.providers(series, season, episode, whitelist, blacklist))

        assert len(providers) > 0, 'no providers found with current settings'

        print('\n')
        data.print_table(providers)
        print('\n')

        try:
            input('press ENTER to store this s{}e{} as last episode or CTRL+C to abort\n'.format(season, episode))

            storage.store(series, season, episode)
        except KeyboardInterrupt:
            print('exiting without storing episode')
            return 137
    except AssertionError as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        exit(main())
    except Exception as e:
        logger.critical(e)
        exit(1)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
