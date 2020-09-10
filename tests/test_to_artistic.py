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
_ZBAR = False
try:
    from pyzbar.pyzbar import decode as zbardecode
    _ZBAR = True
except ImportError:
    pass


def decode(img):
    decoded = zbardecode(img)
    assert 1 == len(decoded)
    assert 'QRCODE' == decoded[0].type
    return decoded[0].data.decode('utf-8')


if not _ZBAR:
    def decode(img):  # noqa: F811
        import warnings
        warnings.warn('pyzbar not available')
        return True


def _img_src(name):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), 'artistic', name)


def _make_tmp_filename(ext):
    f = tempfile.NamedTemporaryFile('wb', suffix='.' + ext, delete=False)
    return f.name


def test_animated():
    content = 'Ring my friend'
    qr = segno.make_qr(content)
    scale = 8
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('gif')
    qr.to_artistic(_img_src('animated.gif'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
        assert img.is_animated
    finally:
        os.remove(fn)
    assert content == decode(img)


def test_transparency():
    content = "Day or night, he'll be there any time at all"
    qr = segno.make_qr(content)
    scale = 3
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
    assert content == decode(img)


def test_transparency_to_rgb():
    content = "You're a new and better man"
    qr = segno.make_qr(content)
    scale = 5
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
    assert content == decode(img)


def test_jpeg():
    content = "If you're down, he'll pick you up"
    qr = segno.make_qr(content)
    scale = 7
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('jpg')
    qr.to_artistic(_img_src('sunflower.jpg'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
    finally:
        os.remove(fn)
    assert content == decode(img)


def test_jpeg_to_png():
    content = "Doctor Robert"
    qr = segno.make_qr(content)
    scale = 3
    width, height = qr.symbol_size(scale=scale)
    fn = _make_tmp_filename('png')
    qr.to_artistic(_img_src('sunflower.jpg'), fn, scale=scale)
    img = Image.open(fn)
    try:
        assert (width, height) == img.size
    finally:
        os.remove(fn)
    assert content == decode(img)


if __name__ == '__main__':
    pytest.main([__file__])
