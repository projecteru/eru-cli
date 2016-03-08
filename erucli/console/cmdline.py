# coding: utf-8
import os
import urlparse

import click
import pygit2
import yaml
from eruhttp import EruClient

from erucli.console.commands import commands
from erucli.console.style import error


def create_http_git_clone_url(clone_url, scheme='http'):
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


def create_ssh_git_clone_url(clone_url):
    """
    >>> create_ssh_git_clone_url('https://github.com/neovim/neovim.git')
    'git@github.com:neovim/neovim.git'
    """
    if clone_url.startswith('git'):
        return clone_url
    parsed = urlparse.urlparse(clone_url, 'https')
    netloc, path = parsed.netloc, parsed.path
    ssh_clone_url = 'git@' + netloc + ':' + path.lstrip('/')
    return ssh_clone_url


def make_absolute_path(domain_name_or_url):
    """
    >>> make_absolute_path('127.0.0.1')
    'http://127.0.0.1'
    >>> make_absolute_path('http://127.0.0.1:10086/')
    'http://127.0.0.1:10086'
    """
    parsed = urlparse.urlparse(domain_name_or_url, 'http')
    netloc = parsed.netloc or parsed.path
    parse_result = urlparse.ParseResult('http', netloc, '', *parsed[3:])
    return parse_result.geturl()



@click.group()
@click.option('--clone-url-type', type=click.Choice(['http', 'https', 'ssh']), default='http')
@click.pass_context
def eru_commands(ctx, clone_url_type):
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
    if clone_url_type.startswith('http'):
        ctx.obj['remote']  = create_http_git_clone_url(origin_remote_url, clone_url_type)
    else:
        ctx.obj['remote']  = create_ssh_git_clone_url(origin_remote_url)

    eru_absolute_path = make_absolute_path(eru_url)
    ctx.obj['eru'] = EruClient(eru_absolute_path)


for command, function in commands.iteritems():
    eru_commands.command(command)(function)


def main():
    eru_commands(obj={})
