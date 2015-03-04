# coding: utf-8

import os
import click
import yaml
import pygit2

from nbe.client import EruClient
from nbe.console.style import error
from nbe.console.app import (register_app_version, set_app_env, list_app_env,
        deploy_private_container, deploy_public_container, build_image)

@click.group()
@click.argument('eru_url', envvar='ERU_URL')
@click.pass_context
def nbecommands(ctx, eru_url):
    if not os.path.exists(os.path.abspath('./.git')):
        click.echo(error('Must run inside git dir'))
        ctx.exit(-1)
    if not os.path.exists(os.path.abspath('./app.yaml')):
        click.echo(error('Need app.yaml in repository'))
        ctx.exit(-1)

    with open(os.path.abspath('./app.yaml')) as f:
        appconfig = yaml.load(f)
        ctx.obj['appconfig'] = appconfig
        ctx.obj['appname'] = appconfig['appname']

    repo = pygit2.Repository('.')
    ctx.obj['sha1'] = repo.head.target
    ctx.obj['short_sha1'] = repo.head.target[:7]

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

nbecommands.command('app:register')(register_app_version)
nbecommands.command('app:setenv')(set_app_env)
nbecommands.command('app:listenv')(list_app_env)
nbecommands.command('app:dpri')(deploy_private_container)
nbecommands.command('app:dpub')(deploy_public_container)
nbecommands.command('app:build')(build_image)

def main():
    nbecommands(obj={})

