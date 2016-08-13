# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against Segno PIL/Pillow.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
from nose.tools import ok_, eq_
import segno


def test_pil():
    qr = segno.make_qr('A')
    img = qr.to_pil()
    ok_(img)
    width, height = qr.symbol_size()
    eq_((width, height), img.size)
    eq_('1', img.mode)


def test_pil_color():
    qr = segno.make_qr('A')
    img = qr.to_pil(color='green')
    ok_(img)
    eq_('P', img.mode)


def test_pil_color_black():
    qr = segno.make_qr('A')
    img = qr.to_pil(color='#000')
    ok_(img)
    eq_('1', img.mode, 'Expected greyscale image')


def test_pil_greyscale_mirrored():
    qr = segno.make_qr('A')
    img = qr.to_pil(color='#fff', background='#000')
    ok_(img)
    eq_('1', img.mode, 'Expected greyscale image')


def test_pil_pal_background():
    qr = segno.make('Hello')
    img = qr.to_pil(color='white', background='green')
    ok_(img)
    eq_('P', img.mode)


def test_pil_scale():
    qr = segno.make_qr('A')
    scale = 4
    width, height = qr.symbol_size(scale=scale)
    img = qr.to_pil(scale=scale)
    eq_((width, height), img.size)


def test_pil_scale_float():
    qr = segno.make_qr('A')
    scale = 2.5
    width, height = qr.symbol_size(scale=int(scale))
    img = qr.to_pil(scale=scale)
    eq_((width, height), img.size)


def test_pil_border():
    qr = segno.make_qr('A')
    border = 0
    width, height = qr.symbol_size(border=border)
    img = qr.to_pil(border=border)
    eq_((width, height), img.size)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
