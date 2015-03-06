# coding: utf-8

import click

from nbe.console.style import info

def as_form(title, content, width):
    click.echo(info(''.join(t.ljust(width) for t in title)))
    click.echo(info('-' * len(title) * width))
    for line in content:
        click.echo(''.join(l.ljust(width) for l in line))

