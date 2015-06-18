# coding: utf-8

import time
import click
import humanize
from datetime import datetime
from eruhttp import EruException

from erucli.console.style import error, info
from erucli.console.output import as_form

@click.pass_context
@click.option('--raw', '-r', help='deploy a raw image', is_flag=True)
def register_app_version(ctx, raw):
    eru = ctx.obj['eru']
    try:
        eru.register_app_version(
            ctx.obj['appname'],
            ctx.obj['sha1'],
            ctx.obj['remote'],
            ctx.obj['appname'],
            ctx.obj['appconfig'],
            raw
        )
        click.echo(info('Register successfully'))
    except EruException as e:
        click.echo(error(e.message))

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
    try:
        eru.set_app_env(ctx.obj['appname'], env, **kv)
        click.echo(info('env variables set successfully'))
    except EruException as e:
        click.echo(error(e.message))

@click.argument('env')
@click.pass_context
def list_app_env_content(ctx, env):
    eru = ctx.obj['eru']
    try:
        r = eru.list_app_env_content(ctx.obj['appname'], env)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Key', 'Value']
        data = r['data']
        content = [(key, data.get(key, '')) for key in sorted(data.keys())]
        as_form(title, content)

@click.pass_context
def list_app_containers(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    try:
        r = eru.list_app_containers(name)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Name', 'Time', 'Entry', 'Version', 'Alive', 'Host', 'Backends', 'ID']
        content = [
            [
                c['name'],
                humanize.naturaltime(datetime.strptime(c['created'], '%Y-%m-%d %H:%M:%S')),
                c['entrypoint'],
                c['version'],
                'yes' if c['is_alive'] else 'no', 
                c['host'],
                ','.join(n['address'] for n in c['networks']) or '-',
                c['container_id'][:7]
            ] for c in r['containers']
        ]
        as_form(title, content)

@click.pass_context
def list_app_env_names(ctx):
    eru = ctx.obj['eru']
    name = ctx.obj['appname']
    try:
        r = eru.list_app_env_names(name)
    except EruException as e:
        click.echo(error(e.message))
    else:
        title = ['Env', ]
        content = [[e, ] for e in r['data']]
        as_form(title, content)

@click.argument('group')
@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncore', '-c', default=1, help='how many cores per container', type=float)
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.option('--network', '-i', help='version to deploy', multiple=True)
@click.option('--host', '-h', help='specific host name', default=None, type=str)
@click.option('--ip', '-p', help='specific ip', multiple=True)
@click.option('--raw', '-r', help='deploy a raw image', is_flag=True)
@click.option('--image', '-m', help='specific image', default='', type=str)
@click.pass_context
def deploy_private_container(ctx, group, pod, entrypoint,
        env, ncore, ncontainer, version, network, host, ip, raw, image):
    eru = ctx.obj['eru']

    network_ids = []
    for nname in network:
        try:
            n = eru.get_network(nname)
        except EruException as e:
            click.echo(error(e.message))
            ctx.exit(-1)
        else:
            network_ids.append(n['id'])

    if not version:
        version = ctx.obj['short_sha1']
    try:
        r = eru.deploy_private(
            group,
            pod,
            ctx.obj['appname'],
            ncore,
            ncontainer,
            version,
            entrypoint,
            env,
            network_ids,
            host,
            raw,
            image,
            ip
        )
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)

        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))

@click.argument('group')
@click.argument('pod')
@click.argument('entrypoint')
@click.option('--env', '-e', default='prod', help='run env')
@click.option('--ncontainer', '-n', default=1, help='how many containers', type=int)
@click.option('--version', '-v', default=None, help='version to deploy')
@click.option('--network', '-i', help='version to deploy', multiple=True)
@click.option('--ip', '-p', help='specific ip', multiple=True)
@click.option('--raw', '-r', help='deploy a raw image', is_flag=True)
@click.option('--image', '-m', help='specific image', default='', type=str)
@click.pass_context
def deploy_public_container(ctx, group, pod, entrypoint, env, ncontainer,
        version, network, ip, raw, image):
    eru = ctx.obj['eru']

    network_ids = []
    for nname in network:
        try:
            n = eru.get_network(nname)
        except EruException as e:
            click.echo(error(e.message))
            ctx.exit(-1)
        else:
            network_ids.append(n['id'])

    if not version:
        version = ctx.obj['short_sha1']

    try:
        r = eru.deploy_public(
            group,
            pod,
            ctx.obj['appname'],
            ncontainer,
            version,
            entrypoint,
            env,
            network_ids,
            raw,
            image,
            ip
        )
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)
        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))

@click.argument('group')
@click.argument('pod')
@click.argument('base')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def build_image(ctx, group, pod, base, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    try:
        r = eru.build_image(group, pod, ctx.obj['appname'], base, version)
    except EruException as e:
        click.echo(error(e.message))
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
    try:
        r = eru.remove_containers(container_ids)
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)
        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))

@click.argument('group')
@click.argument('pod')
@click.option('--version', '-v', default=None, help='version to deploy')
@click.pass_context
def offline_version(ctx, group, pod, version):
    eru = ctx.obj['eru']
    if not version:
        version = ctx.obj['short_sha1']
    try:
        r = eru.offline_version(group, pod, ctx.obj['appname'], version)
    except EruException as e:
        click.echo(error(e.message))
        return

    count = 1
    task_status = {i: 0 for i in r['tasks']}
    while not all(s != 0 for s in task_status.values()):
        if count < 10:
            click.echo('o' * count + '\r', nl=False)
        elif count % 2:
            click.echo('o' * 10 + 'o\r', nl=False)
        else:
            click.echo('o' * 10 + 'x\r', nl=False)
        for task_id, status in task_status.iteritems():
            if status != 0:
                continue
            try:
                task = eru.get_task(task_id)
                if task['finished']:
                    task_status[task_id] = 1
            except EruException:
                task_status[task_id] = -1
        time.sleep(0.5)
        count += 1

    fcount = len([s for s in task_status.values() if s == -1])
    scount = len([s for s in task_status.values() if s == 1])
    click.echo(info('Done.' + count * ' '))
    click.echo(info('%s failed, %s succeeded.' % (fcount, scount)))
