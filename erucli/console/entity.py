# coding: utf-8

import click

from erucli.console.style import error, info

@click.argument('name')
@click.argument('description', default='')
@click.pass_context
def create_group(ctx, name, description):
    eru = ctx.obj['eru']
    r = eru.create_group(name, description)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Group created successfully'))

@click.argument('name')
@click.argument('description', default='')
@click.pass_context
def create_pod(ctx, name, description):
    eru = ctx.obj['eru']
    r = eru.create_pod(name, description)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Pod created successfully'))

@click.argument('name')
@click.argument('netspace')
@click.pass_context
def create_network(ctx, name, netspace):
    eru = ctx.obj['eru']
    r = eru.create_network(name, netspace)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Network created successfully'))

@click.argument('pod_name')
@click.argument('group_name')
@click.pass_context
def assign_pod_to_group(ctx, pod_name, group_name):
    eru = ctx.obj['eru']
    r = eru.assign_pod_to_group(pod_name, group_name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Pod assigned to group successfully'))

@click.argument('addr')
@click.argument('pod_name')
@click.pass_context
def create_host(ctx, addr, pod_name):
    eru = ctx.obj['eru']
    r = eru.create_host(addr, pod_name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Host created successfully'))


@click.argument('addr')
@click.argument('group_name')
@click.pass_context
def assign_host_to_group(ctx, addr, group_name):
    eru = ctx.obj['eru']
    r = eru.assign_host_to_group(addr, group_name)
    if r['r']:
        click.echo(error(r['msg']))
    else:
        click.echo(info('Host assigned to group successfully'))

