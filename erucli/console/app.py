# coding: utf-8

import click

from erucli.console.style import error, info
from erucli.console.output import as_form

@click.pass_context
def register_app_version(ctx):
    eru = ctx.obj['eru']
    r = eru.register_app_version(ctx.obj['appname'], ctx.obj['sha1'],
            ctx.obj['remote'], ctx.obj['appname'], ctx.obj['appconfig'])
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
def list_app_env_content(ctx, env):
    eru = ctx.obj['eru']
    r = eru.list_app_env_content(ctx.obj['appname'], env)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        title = ['Key', 'Value']
        data = r['data']
        content = [(key, data.get(key, '')) for key in sorted(data.keys())]
        as_form(title, content)

@click.pass_context
def list_app_containers(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    r = eru.list_app_containers(name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        title = ['Name', 'Time', 'Entry', 'Version', 'Alive', 'Host', 'ID']
        content = [[c['name'], c['created'],
            c['entrypoint'], c['version'],
            'yes' if c['is_alive'] else 'no', 
            c['host'], c['container_id'][:7]] for c in r['containers']]
        as_form(title, content)

@click.pass_context
def list_app_env_names(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    r = eru.list_app_env_names(name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        title = ['Env', ]
        content = [[e, ] for e in r['data']]
        as_form(title, content)

@click.argument('env')
@click.argument('res_name')
@click.option('--name', '-n', default='')
@click.pass_context
def alloc_resource(ctx, env, res_name, name):
    if name == '':
        name = res_name
    if res_name not in ('influxdb', 'mysql'):
        click.echo(error('Res name must be influxdb/mysql'))
        ctx.exit(-1)
    eru = ctx.obj['eru']
    r = eru.alloc_resource(ctx.obj['appname'], env, res_name, name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Alloc successfully'))

@click.argument('group')
@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncore', '-c', default=1, help='how many cores per container', type=float)
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.option('--network', '-i', help='version to deploy', multiple=True)
@click.pass_context
def deploy_private_container(ctx, group, pod, entrypoint, env, ncore, ncontainer, version, network):
    eru = ctx.obj['eru']

    network_ids = []
    for nname in network:
        n = eru.get_network_by_name(nname)
        if 'r' in n and n['r'] == 1:
            click.echo(error(n['msg']))
            ctx.exit(-1)
        network_ids.append(n['id'])

    if not version:
        version = ctx.obj['short_sha1']
    r = eru.deploy_private(group, pod, ctx.obj['appname'], ncore,
            ncontainer, version, entrypoint, env, network_ids)
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
@click.option('--network', '-i', help='version to deploy', multiple=True)
@click.pass_context
def deploy_public_container(ctx, group, pod, entrypoint, env, ncontainer, version, network):
    eru = ctx.obj['eru']

    network_ids = []
    for nname in network:
        n = eru.get_network_by_name(nname)
        if 'r' in n and n['r'] == 1:
            click.echo(error(n['msg']))
            ctx.exit(-1)
        network_ids.append(n['id'])

    if not version:
        version = ctx.obj['short_sha1']
    r = eru.deploy_public(group, pod, ctx.obj['appname'],
            ncontainer, version, entrypoint, env, network_ids)
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
        for d in eru.build_log(r['task']):
            if 'stream' in d:
                click.echo(d['stream'], nl=False)
            elif 'status' in d:
                status = d['status']
                progress = d.get('progress', '')
                if progress:
                    click.echo('%s, %s      \r' % (status, progress), nl=False)
                else:
                    click.echo(status)

@click.argument('task')
@click.pass_context
def build_log(ctx, task):
    eru = ctx.obj['eru']
    for d in eru.build_log(task):
        if 'stream' in d:
            click.echo(d['stream'], nl=False)
        elif 'status' in d:
            status = d['status']
            progress = d.get('progress', '')
            if progress:
                click.echo('%s, %s      \r' % (status, progress), nl=False)
            else:
                click.echo(status)

@click.argument('container_id')
@click.option('--stdout', '-o', is_flag=True)
@click.option('--stderr', '-e', is_flag=True)
@click.option('--tail', '-t', default=10)
@click.pass_context
def container_log(ctx, container_id, stdout, stderr, tail):
    eru = ctx.obj['eru']
    if not stdout and not stderr:
        click.echo(error('Set at least one in --stdout/--stderr'))
        ctx.exit(-1)
    for line in eru.container_log(container_id, int(stdout), int(stderr), tail):
        click.echo(line, nl=False)

@click.argument('container_ids', nargs=-1)
@click.pass_context
def remove_containers(ctx, container_ids):
    eru = ctx.obj['eru']
    r = eru.remove_containers(container_ids)
    if r['r']:
        click.echo(error(r['msg']))
    else:
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

@click.argument('group')
@click.argument('pod')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def update_version(ctx, group, pod, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    r = eru.update_version(group, pod, ctx.obj['appname'], version)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        # TODO get tasks id
        click.echo(info('Update successfully'))

