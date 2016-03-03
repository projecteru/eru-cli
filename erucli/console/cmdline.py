# coding: utf-8
import os
import urlparse

import click
import pygit2
import yaml
from eruhttp import EruClient

from erucli.console.commands import commands
from erucli.console.style import error


def create_http_git_clone_url(clone_url):
    """
    >>> create_http_git_clone_url('git@github.com:projecteru/eru-cli.git')
    'http://github.com/projecteru/eru-cli.git'
    """
    if clone_url.startswith('http'):
        return clone_url
    # assume clone_url is like 'git@xxx.com:username/repo-name.git
    _, path = clone_url.split('@', 1)
    http_clone_url = 'http://' + path.replace(':', '/')
    return http_clone_url


def make_absolute_path(domain_name_or_url):
    """
    >>> make_absolute_path('127.0.0.1')
    'http://127.0.0.1'
    >>> make_absolute_path('http://127.0.0.1:10086/')
    'http://127.0.0.1:10086'
    """
    p = urlparse.urlparse(domain_name_or_url, 'http')
    netloc = p.netloc or p.path
    p = urlparse.ParseResult('http', netloc, '', *p[3:])
    return p.geturl()


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
    # 有时候app.yaml里会写version的, 就以他为主了
    ctx.obj['sha1'] = appconfig.get('version', '') or repo.head.target.hex
    ctx.obj['short_sha1'] = appconfig.get('version', '')[:7] or ctx.obj['sha1'][:7]

    origin_remote_url = next(r.url for r in repo.remotes if r.name == 'origin')
    ctx.obj['remote']  = create_http_git_clone_url(origin_remote_url)

    eru_absolute_path = make_absolute_path(eru_url)
    ctx.obj['eru'] = EruClient(eru_absolute_path)

for command, function in commands.iteritems():
    eru_commands.command(command)(function)


def main():
    eru_commands(obj={})
