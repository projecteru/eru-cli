# coding: utf-8

import click
from tabulate import tabulate

from erucli.console.style import info

def as_form(title, content):
    empty = not bool(content)
    if empty:
        content = [['' for _ in title]]
    header, contents = tabulate(content, headers=title).split('-\n', 1) # tricky
    click.echo(info(header + '-'))
    if not empty:
        click.echo(contents)

