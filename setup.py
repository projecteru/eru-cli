# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='nbecli',
    version='0.1',
    author='tonic',
    zip_safe=False,
    author_email='tonic@wolege.ca',
    description='NBE command line tool',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':['nbe=nbe.console.cmdline:main'],
    },
    install_requires=[
        'click>=2.0',
        'requests>=2.2.1',
        'PyYAML',
        'pygit2',
        'websocket',
    ],
)
