#!/usr/bin/env python

import os
from setuptools import setup, find_packages

DIRPATH = os.path.dirname(os.path.abspath(__file__))


def get_requiremenets():
    file_path = os.path.join(DIRPATH, 'requirements.txt')
    result = []
    with open(file_path, 'r') as f:
        for line in f:
            line = line.split('#', 1)[0].strip()
            if len(line) == 0:
                continue
            if line.startswith('--'):
                continue
            result.append(line)
    return result


setup(
    name='cskatebot',
    version='0.0.1',
    description='Chaseskate telegram bot',
    author='Andrey Proskurnev',
    author_email='andrey@proskurnev.ru',
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=get_requiremenets(),
    entry_points={
        'console_scripts': [
            'cskatebot = cskatebot.ctl:main',
        ],
    },
)
