# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Tests against QRCode.to_artistic
"""
from __future__ import absolute_import
import os
import tempfile
from PIL import Image
import pytest
import segno


def _img_src(name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'artistic', name)


def _make_tmp_filename(ext):
    f = tempfile.NamedTemporaryFile('wb', suffix='.' + ext, delete=False)
    print(f.name)
    return f.name


def test_animated():
    qr = segno.make_qr('A')
    scale = 4
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('gif')
    qr.to_artistic(_img_src('animated.gif'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
        assert img.is_animated
    finally:
        os.remove(fn)


def test_transparency():
    qr = segno.make_qr('A')
    scale = 9
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('png')
    qr.to_artistic(_img_src('transparency.png'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
        try:
            assert not img.is_animated
        except AttributeError:
            pass
    finally:
        os.remove(fn)


def test_transparency_to_rgb():
    qr = segno.make_qr('A')
    scale = 9
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('png')
    src_fn = _img_src('transparency.png')
    img_src = Image.open(src_fn)
    assert 'RGBA' == img_src.mode
    qr.to_artistic(src_fn, fn, scale=scale, mode='RGB')
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
        assert 'RGB' == img.mode
    finally:
        os.remove(fn)


def test_jpeg():
    qr = segno.make_qr('A')
    scale = 27
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('jpg')
    qr.to_artistic(_img_src('sunflower.jpg'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
    finally:
        os.remove(fn)


def test_jpeg_to_png():
    qr = segno.make_qr('A')
    scale = 5
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('png')
    qr.to_artistic(_img_src('sunflower.jpg'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
    finally:
        os.remove(fn)


if __name__ == '__main__':
    pytest.main([__file__])
