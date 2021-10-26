#!/usr/bin/env python

import codecs
from os import path
from platform import system

from setuptools import setup

with open('requirements.txt') as f:
    install_requires = f.readlines()

VERSION = "0.1"

setup(
    name='fix-atlassian-links',
    version=VERSION,
    description='CLI tool to fix links in Atlassian tools like Confluence, Jira, etc',
    long_description=codecs.open(
        path.join(path.abspath(path.dirname(__file__)), 'README.md'),
        mode='r',
        encoding='utf-8'
    ).read(),
    url='https://github.com/pwillis-els/fix-atlassian-links.git',
    packages=['fix_atlassian_links'],
    setup_requires=[
        'setuptools',
    ],
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['fix-atlassian-links=fix_atlassian_links.main:Main']
    },
    include_package_data=True,
    python_requires='>=3.2'
)

