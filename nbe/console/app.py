# coding: utf-8

import click

from nbe.console.style import error, info

@click.pass_context
def register_app_version(ctx):
    eru = ctx.obj['eru']
    r = eru.register_app_version(ctx.obj['appname'], ctx.obj['sha1'],
            ctx.obj['remote'], '', ctx.obj['appconfig'])
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Register successfully'))

@click.argument('env', help='environment')
@click.argument('vs', nargs=-1, help='env variables')
@click.pass_context
def set_app_env(ctx, env, vs):
    kv = {}
    for v in vs:
        if not '=' in v:
            click.echo(error('Env must be like key=value'))
            ctx.exit(-1)
        key, value = v.split('=', 1)
        kv[key] = value
    eru = ctx.obj['eru']
    r = eru.set_app_env(ctx.obj['appname'], env, **kv)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('env variables set successfully'))

@click.argument('env', help='environment')
@click.pass_context
def list_app_env(ctx, env):
    eru = ctx.obj['eru']
    r = eru.list_app_env(ctx.obj['appname'], env)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        for key, value in r['data'].iteritems():
            click.echo('{0} = {1}'.format(key, value))

@click.argument('group', help='group name')
@click.argument('pod', help='pod name')
@click.argument('entrypoint', help='entrypoint in app.yaml')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncore', '-c', default=1, help='how many cores per container', type=int)
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
def deploy_private_container(ctx, group, pod, entrypoint, env, ncore, ncontainer, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.deploy_private(group, pod, ctx.obj['appname'], ncore,
            ncontainer, version, entrypoint, env)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Deploy successfully'))

@click.argument('group', help='group name')
@click.argument('pod', help='pod name')
@click.argument('entrypoint', help='entrypoint in app.yaml')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
def deploy_public_container(ctx, group, pod, entrypoint, env, ncontainer, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.deploy_private(group, pod, ctx.obj['appname'],
            ncontainer, version, entrypoint, env)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Deploy successfully'))

@click.argument('group', help='group name')
@click.argument('pod', help='pod name')
@click.argument('base', help='base image')
@click.option('--version', '-v', default=None, help='version to deploy')
def build_image(ctx, group, pod, base, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.build_image(group, pod, ctx.obj['appname'], base, version)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Build successfully'))

