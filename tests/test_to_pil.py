# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against Segno PIL/Pillow.
"""
from __future__ import absolute_import
import pytest
import segno


def test_pil():
    qr = segno.make_qr('A')
    img = qr.to_pil()
    assert img
    width, height = qr.symbol_size()
    assert (width, height) == img.size
    assert '1' == img.mode


def test_pil_color():
    qr = segno.make_qr('A')
    img = qr.to_pil(dark='green')
    assert img
    assert 'P' == img.mode


def test_pil_color_black():
    qr = segno.make_qr('A')
    img = qr.to_pil(dark='#000')
    assert img
    assert '1' == img.mode, 'Expected greyscale image'
    assert qr.symbol_size() == img.size


def test_pil_greyscale_mirrored():
    qr = segno.make_qr('A')
    img = qr.to_pil(dark='#fff', light='#000')
    assert img
    assert '1' == img.mode, 'Expected greyscale image'
    assert qr.symbol_size() == img.size


def test_pil_pal_background():
    qr = segno.make('Hello')
    img = qr.to_pil(dark='white', light='green')
    assert img
    assert 'P' == img.mode
    assert qr.symbol_size() == img.size


def test_pil_scale():
    qr = segno.make_qr('A')
    scale = 4
    width, height = qr.symbol_size(scale=scale)
    img = qr.to_pil(scale=scale)
    assert (width, height) == img.size


def test_pil_scale_float():
    qr = segno.make_qr('A')
    scale = 2.5
    width, height = qr.symbol_size(scale=int(scale))
    img = qr.to_pil(scale=scale)
    assert (width, height) == img.size


def test_pil_border():
    qr = segno.make_qr('A')
    border = 0
    width, height = qr.symbol_size(border=border)
    img = qr.to_pil(border=border)
    assert (width, height) == img.size


def test_pil_transparent():
    qr = segno.make_qr('A')
    img = qr.to_pil(light=None)  # color = black is implicit
    assert img
    assert '1' == img.mode
    assert qr.symbol_size() == img.size
    assert 'transparency' in img.info


def test_pil_color_black_tranparent():
    qr = segno.make_qr('A')
    img = qr.to_pil(dark='black', light=None)
    assert img
    assert '1' == img.mode
    assert qr.symbol_size() == img.size
    assert 'transparency' in img.info


def test_pil_color_white_transparent():
    qr = segno.make_qr('A')
    img = qr.to_pil(dark='#fff', light=None)
    assert img
    assert '1' == img.mode
    assert qr.symbol_size() == img.size
    assert 'transparency' in img.info


def test_pil_color_other_transparent():
    qr = segno.make_qr('A')
    img = qr.to_pil(dark='green', light=None)
    assert img
    assert 'P' == img.mode, 'Expected indexed-color image'
    assert qr.symbol_size() == img.size
    assert 'transparency' in img.info


def test_pil_palette_autodetect():
    qr = segno.make('Segno')
    img = qr.to_pil(dark='#00fc', light=None, border=0)
    assert img
    assert 'P' == img.mode, 'Expected indexed-color image'
    assert qr.symbol_size(border=0) == img.size
    assert 'transparency' in img.info


if __name__ == '__main__':
    pytest.main([__file__])
