# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Nox test runner configuration.
"""
import os
from functools import partial
import nox

nox.options.sessions = ['test-2.7', 'test-3.7']
default_py = '3.7'


@nox.session(python=['2.7', '3.7', '3.8'])
def test(session):
    """\
    Run test suite.
    """
    session.install('-Ur', 'requirements-testing.txt')
    session.install('.')
    session.run('py.test')


@nox.session(python=default_py)
def coverage(session):
    """\
    Run coverage.
    """
    session.install('coverage', '-Ur', 'requirements-testing.txt')
    session.install('.')
    output_dir = os.path.abspath(os.path.join(session.create_tmp(), 'html'))
    cover = partial(session.run, 'coverage')
    cover('erase')
    cover('run', '-m', 'pytest')
    cover('report')
    cover('html', '-d', output_dir)


@nox.session(python=default_py)
def lint(session):
    """\
    Run flake8
    """
    session.install('flake8')
    session.run('flake8', 'qrcode_artistic.py')
