#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))


def make_readme(root_path):
    FILES = ('README.rst', 'LICENSE', 'CHANGELOG', 'CONTRIBUTORS')
    for filename in FILES:
        filepath = os.path.realpath(os.path.join(HERE, filename))
        if os.path.isfile(filepath):
            with open(filepath, mode='r') as f:
                yield f.read()


LONG_DESCRIPTION = "\r\n\r\n----\r\n\r\n".join(make_readme(HERE))


setup(
    name='screenslop',
    version='0.1.0',
    py_modules=(
        'screenslop',
    ),
    packages=(),
    entry_points={
        'console_scripts': (
            ['screenslop = screenslop:run_via_cmd_line'],
        )
    },
    install_requires=(
        'Pillow>=1.7.7',
        'selenium>=2.44.0',
    ),
    author='Keryn Knight',
    author_email='python-package@kerynknight.com',
    description="Quick and dirty screenshotting from selenium @ N viewport sizes",
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    zip_safe=False,
    license="BSD License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
