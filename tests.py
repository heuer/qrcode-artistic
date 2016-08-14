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
from nose.tools import ok_, eq_, raises
import segno
from segno import colors


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
    eq_(qr.symbol_size(), img.size)


def test_pil_greyscale_mirrored():
    qr = segno.make_qr('A')
    img = qr.to_pil(color='#fff', background='#000')
    ok_(img)
    eq_('1', img.mode, 'Expected greyscale image')
    eq_(qr.symbol_size(), img.size)


def test_pil_greyscale_but_force_palette():
    qr = segno.make_qr('A')
    img = qr.to_pil(color='#000', mode='P')
    ok_(img)
    eq_('P', img.mode, 'Expected indexed-color image')
    eq_(qr.symbol_size(), img.size)


def test_pil_pal_background():
    qr = segno.make('Hello')
    img = qr.to_pil(color='white', background='green')
    ok_(img)
    eq_('P', img.mode)
    eq_(qr.symbol_size(), img.size)


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


def test_pil_transparent():
    qr = segno.make_qr('A')
    color = 'black'
    color_rgb = colors.color_to_rgb(color)
    color_inverse = colors.invert_color(color_rgb)
    img = qr.to_pil(background=None)  # color = black is implicit
    ok_(img)
    eq_('P', img.mode, 'Expected indexed-color img')
    eq_(qr.symbol_size(), img.size)
    palette = img.getpalette()
    eq_(color_inverse, tuple(palette[:3]))  # 1st entry: background
    eq_(color_rgb, tuple(palette[3:6]))     # 2nd entry: stroke color


def test_pil_color_black_tranparent():
    qr = segno.make_qr('A')
    color = 'black'
    color_rgb = colors.color_to_rgb(color)
    color_inverse = colors.invert_color(color_rgb)
    img = qr.to_pil(color=color, background=None)
    ok_(img)
    eq_('P', img.mode, 'Expected indexed-color img')
    eq_(qr.symbol_size(), img.size)
    palette = img.getpalette()
    eq_(color_inverse, tuple(palette[:3]))  # 1st entry: background
    eq_(color_rgb, tuple(palette[3:6]))     # 2nd entry: stroke color


def test_pil_color_white_tranparent():
    qr = segno.make_qr('A')
    color = '#fff'
    color_rgb = colors.color_to_rgb(color)
    color_inverse = colors.invert_color(color_rgb)
    img = qr.to_pil(color=color, background=None)
    ok_(img)
    eq_('P', img.mode, 'Expected indexed-color img')
    eq_(qr.symbol_size(), img.size)
    palette = img.getpalette()
    eq_(color_inverse, tuple(palette[:3]))  # 1st entry: background
    eq_(color_rgb, tuple(palette[3:6]))     # 2nd entry: stroke color


def test_pil_color_other_tranparent():
    qr = segno.make_qr('A')
    color = 'green'
    color_rgb = colors.color_to_rgb(color)
    color_inverse = colors.invert_color(color_rgb)
    img = qr.to_pil(color=color, background=None)
    ok_(img)
    eq_('P', img.mode, 'Expected indexed-color image')
    eq_(qr.symbol_size(), img.size)
    palette = img.getpalette()
    eq_(color_inverse, tuple(palette[:3]))  # 1st entry: background
    eq_(color_rgb, tuple(palette[3:6]))     # 2nd entry: stroke color


def test_pil_rgba_autodetect():
    qr = segno.make('Segno')
    color = '#00fc'
    color_rgba = colors.color_to_rgba(color, alpha_float=False)
    color_inverse = colors.invert_color(color_rgba[:3]) + (0,)
    img = qr.to_pil(color=color, background=None, border=0)
    ok_(img)
    eq_('RGBA', img.mode, 'Expected RGBA image')
    eq_(qr.symbol_size(border=0), img.size)
    eq_(color_rgba, img.getpixel((0, 0)))
    eq_(color_inverse, img.getpixel((1, 1)))


@raises(ValueError)
def test_pil_mode_illegal():
    qr = segno.make('Segno')
    qr.to_pil(scale=10, mode='U')


@raises(ValueError)
def test_pil_mode_illegal2():
    qr = segno.make('Segno')
    qr.to_pil(scale=10, mode='RGB')


def test_pil_mode_force_rgba():
    qr = segno.make('Segno')
    img = qr.to_pil(mode='RGBA')
    eq_('RGBA', img.mode)
    eq_(qr.symbol_size(), img.size)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
