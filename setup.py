#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Setup script.
"""
from __future__ import unicode_literals
from setuptools import setup
import os
import io
import re


def read(*filenames, **kwargs):
    base_path = os.path.dirname(os.path.realpath(__file__))
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(os.path.join(base_path, filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


version = re.search(r'''^__version__ = ["']([^'"]+)['"]''',
                    read('qrcode_artistic.py'), flags=re.MULTILINE).group(1)

setup(
    name='qrcode-artistic',
    version=version,
    url='https://github.com/heuer/qrcode-artistic/',
    description='Artistic (Micro) QR Code plugin for Segno',
    long_description=read('README.rst', 'CHANGES.rst'),
    license='BSD',
    author='Lars Heuer',
    author_email='heuer@semagia.com',
    platforms=['any'],
    py_modules=['qrcode_artistic'],
    entry_points="""
    [segno.plugin.converter]
    pil = qrcode_artistic:write_pil
    artistic = qrcode_artistic:write_artistic
    """,
    install_requires=['segno>=1.0.2', 'Pillow'],
    include_package_data=True,
    keywords=['QR Code', 'Micro QR Code', 'ISO/IEC 18004',
              'ISO/IEC 18004:2006(E)', 'ISO/IEC 18004:2015(E)', 'PIL', 'Pillow'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Printing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
