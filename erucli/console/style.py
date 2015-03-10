# coding: utf-8

import click

def warn(text):
    return click.style(text, fg='yellow')

def error(text):
    return click.style(text, fg='red', bold=True)

def normal(text):
    return click.style(text, fg='white')

def info(text):
    return click.style(text, fg='green')

