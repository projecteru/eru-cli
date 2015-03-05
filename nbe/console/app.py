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

@click.argument('env')
@click.argument('vs', nargs=-1)
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

@click.argument('env')
@click.pass_context
def list_app_env(ctx, env):
    eru = ctx.obj['eru']
    r = eru.list_app_env(ctx.obj['appname'], env)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        for key, value in r['data'].iteritems():
            click.echo('{0} = {1}'.format(key, value))

@click.pass_context
def list_app_containers(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    r = eru.list_app_containers(name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo('Name'.ljust(20) + 'ContainerName'.ljust(30) + 'CreateTime'.ljust(30) + 'ContainerID'.ljust(20))
        click.echo('-' * 100)
        for c in r['containers']:
            click.echo(name.ljust(20) + c['name'].ljust(30) + c['created'].ljust(30) + c['container_id'][:7].ljust(20))

@click.argument('group')
@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncore', '-c', default=1, help='how many cores per container', type=int)
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
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

@click.argument('group')
@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def deploy_public_container(ctx, group, pod, entrypoint, env, ncontainer, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.deploy_public(group, pod, ctx.obj['appname'],
            ncontainer, version, entrypoint, env)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Deploy successfully'))

@click.argument('group')
@click.argument('pod')
@click.argument('base')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
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

@click.argument('group')
@click.argument('pod')
@click.argument('host')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.option('--ncontainer', '-n', default=1, help='amount of containers')
@click.pass_context
def remove_containers(ctx, group, pod, host, version, ncontainer):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.remove_containers(group, pod, ctx.obj['appname'],
            version, host, ncontainer)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Remove successfully'))

@click.argument('group')
@click.argument('pod')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def offline_version(ctx, group, pod, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.offline_version(group, pod, ctx.obj['appname'], version)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Offline successfully'))

