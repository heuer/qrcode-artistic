# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Segno writer plugin to convert a (Micro) QR Code into a PIL/Pillow Image.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD License
"""
from __future__ import absolute_import
from segno.writers import check_valid_scale
from segno.utils import get_border
from segno import colors
try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    try:
        import Image, ImageDraw
    except ImportError:  # pragma: no cover
        import warnings
        warnings.warn('PIL or Pillow is required')
        raise

__version__ = '0.1.0'


def write_pil(qrcode, scale=1, border=None, color='#000', background='#fff'):
    """\
    Converts the provided `qrcode` into a PIL/Pillow image.

    This function creates either a greyscale (PIL/Pillow mode "1") or a
    indexed-color (PIL/Pillow mode "P") image.

    If `background` is ``None`` (transparent) use ``save(..., transparency=0)``
    to save the PIL Image with a transparent background.

    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as hexadecimal
            format (``#RGB`` or ``#RRGGBB``), or web color name (i.e. ``red``).
    :param background: Optional background color (default: white).
            See `color` for valid values. In addition, ``None`` is
            accepted which indicates a transparent background.
    """
    def pil_color(color):
        if color is not None and not isinstance(color, tuple):
            return colors.color_to_rgb(color)
        return color

    scale = int(scale)
    check_valid_scale(scale)
    border = get_border(qrcode.version, border)
    width, height = qrcode.symbol_size(scale, border)
    stroke_col, bg_col = pil_color(color), pil_color(background)
    transparent = background is None
    palette = []
    if transparent:
        bg_col = colors.invert_color(stroke_col)
    is_greyscale = colors.color_is_black(stroke_col) and colors.color_is_white(bg_col)
    is_mirrored = colors.color_is_white(stroke_col) and colors.color_is_black(bg_col)
    is_greyscale = is_greyscale or is_mirrored
    stroke_col, bg_col = 1, 0
    if transparent or not is_greyscale:
        mode = 'P'  # Indexed-color aka Palette mode
        palette.extend(bg_col)
        palette.extend(stroke_col)
    else:
        mode = '1'  # Greyscale mode
        if not is_mirrored:
            stroke_col, bg_col = 0, 1
    img = Image.new(mode, (width, height), bg_col)
    if palette:
        img.putpalette(palette)
    drw = ImageDraw.Draw(img)
    rect = drw.rectangle
    for row_no, row in enumerate(qrcode.matrix):
        for col_no, bit in enumerate(row):
            if not bit:
                continue
            x = (col_no + border) * scale
            y = (row_no + border) * scale
            rect([(x, y), (x + scale - 1, y + scale - 1)], fill=stroke_col)
    return img
