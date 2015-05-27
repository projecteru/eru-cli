# coding: utf-8

import os
import click
import yaml
import pygit2

from eruhttp import EruClient
from erucli.console.style import error
from erucli.console.commands import commands

@click.group()
@click.pass_context
def eru_commands(ctx):
    if not os.path.exists(os.path.abspath('./.git')):
        click.echo(error('Must run inside git dir'))
        ctx.exit(-1)
    if not os.path.exists(os.path.abspath('./app.yaml')):
        click.echo(error('Need app.yaml in repository'))
        ctx.exit(-1)
    eru_url = os.getenv('ERU_URL')
    if not eru_url:
        click.echo(error('Need ERU_URL set in env'))
        ctx.exit(-1)

    with open(os.path.abspath('./app.yaml')) as f:
        appconfig = yaml.load(f)
        ctx.obj['appconfig'] = appconfig
        ctx.obj['appname'] = appconfig['appname']

    repo = pygit2.Repository('.')
    ctx.obj['sha1'] = repo.head.target.hex
    ctx.obj['short_sha1'] = ctx.obj['sha1'][:7]

    remote = ''
    for r in repo.remotes:
        if r.name == 'origin':
            remote = r.url
            if not remote.startswith('http'):
                _, path = remote.split('@', 1)
                # 太丢人了...
                remote = 'http://' + path.replace(':', '/')
    ctx.obj['remote'] = remote

    ctx.obj['eru'] = EruClient(eru_url)

for command, function in commands.iteritems():
    eru_commands.command(command)(function)

def main():
    eru_commands(obj={})

