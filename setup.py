# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='erucli',
    version='0.1.12',
    author='tonic',
    zip_safe=False,
    author_email='tonic@wolege.ca',
    description='ERU command line tool',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts':[
            'eru-cli=erucli.console.cmdline:main',
            'nbe=erucli.console.cmdline:main',
        ],
    },
    install_requires=[
        'click>=2.0',
        'requests>=2.2.1',
        'PyYAML',
        'pygit2==0.20.0',
        'websocket-client',
        'tabulate',
        'eru-py',
        'humanize',
    ],
)
