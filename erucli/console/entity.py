# coding: utf-8

import click
from eruhttp import EruException

from erucli.console.style import error, info

@click.argument('name')
@click.argument('description', default='')
@click.pass_context
def create_group(ctx, name, description):
    eru = ctx.obj['eru']
    try:
        eru.create_group(name, description)
        click.echo(info('Group created successfully'))
    except EruException as e:
        click.echo(error(e.message))

@click.argument('name')
@click.argument('description', default='')
@click.pass_context
def create_pod(ctx, name, description):
    eru = ctx.obj['eru']
    try:
        eru.create_pod(name, description)
        click.echo(info('Pod created successfully'))
    except EruException as e:
        click.echo(error(e.message))

@click.argument('name')
@click.argument('netspace')
@click.pass_context
def create_network(ctx, name, netspace):
    eru = ctx.obj['eru']
    try:
        eru.create_network(name, netspace)
        click.echo(info('Network created successfully'))
    except EruException as e:
        click.echo(error(e.message))

@click.argument('pod_name')
@click.argument('group_name')
@click.pass_context
def assign_pod_to_group(ctx, pod_name, group_name):
    eru = ctx.obj['eru']
    try:
        eru.assign_pod_to_group(pod_name, group_name)
        click.echo(info('Pod assigned to group successfully'))
    except EruException as e:
        click.echo(error(e.message))

@click.argument('addr')
@click.argument('pod_name')
@click.pass_context
def create_host(ctx, addr, pod_name):
    eru = ctx.obj['eru']
    try:
        eru.create_host(addr, pod_name)
        click.echo(info('Host created successfully'))
    except EruException as e:
        click.echo(error(e.message))

@click.argument('addr')
@click.argument('group_name')
@click.pass_context
def assign_host_to_group(ctx, addr, group_name):
    eru = ctx.obj['eru']
    try:
        eru.assign_host_to_group(addr, group_name)
        click.echo(info('Host assigned to group successfully'))
    except EruException as e:
        click.echo(error(e.message))

