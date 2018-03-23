# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2018 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# License: BSD License
#
"""\
Segno writer plugin to convert a (Micro) QR Code into a PIL/Pillow Image.
"""
from __future__ import absolute_import
from segno import colors, utils
try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    try:
        import Image, ImageDraw
    except ImportError:  # pragma: no cover
        import warnings
        warnings.warn('PIL or Pillow is required')
        raise

__version__ = '0.1.7.dev0'


_SUPPORTED_MODES = (None, 'P', 'RGBA')


def write_pil(qrcode, scale=1, border=None, color='#000', background='#fff',
              mode=None):
    """\
    Converts the provided `qrcode` into a PIL/Pillow image.

    This function creates either a greyscale (PIL/Pillow mode "1"), an
    indexed-color (PIL/Pillow mode "P") or RGBA image.

    If `background` is ``None`` (transparent) and the image uses mode "P",
    use ``save(..., transparency=0)`` to save the PIL Image with a transparent
    background (background color is always the first entry in the palette).

    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param color: Color of the modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as hexadecimal
            format (``#RGB``, ``#RRGGBB`` ``RRGGBBAA``), or web color
            name (i.e. ``red``).
    :param background: Optional background color (default: white).
            See `color` for valid values. If background is set to ``None`` the
            background will be transparent.
    :param mode: A PIL Image mode. Either ``None`` (default) to autodetect the
            mode or 'P' or 'RGBA'.
    """
    def pil_color(clr):
        if clr is not None and not isinstance(clr, tuple):
            return colors.color_to_rgb_or_rgba(clr, alpha_float=False)
        return clr

    if mode not in _SUPPORTED_MODES:
        raise ValueError('Unsupported mode "{0}", use one of these: {1}' \
                         .format(mode, _SUPPORTED_MODES))
    scale = int(scale)
    utils.check_valid_scale(scale)
    border = qrcode.default_border_size if border is None else border
    width, height = qrcode.symbol_size(scale, border)
    stroke_col, bg_col = pil_color(color), pil_color(background)
    palette = []
    is_greyscale = False
    is_mirrored = False
    if bg_col is None:
        bg_col = colors.invert_color(stroke_col[:3])
        if len(stroke_col) == 4 or mode == 'RGBA':
            bg_col += (0,)
    else:
        is_greyscale = colors.color_is_black(stroke_col) and colors.color_is_white(bg_col)
        is_mirrored = colors.color_is_white(stroke_col) and colors.color_is_black(bg_col)
        is_greyscale = is_greyscale or is_mirrored
    if mode == 'RGBA' or len(stroke_col) == 4 or len(bg_col) == 4:
        mode = 'RGBA'
    elif not is_greyscale or mode == 'P':
        mode = 'P'  # Indexed-color aka Palette mode
        palette.extend(bg_col)
        palette.extend(stroke_col)
        stroke_col, bg_col = 1, 0
    else:
        mode = '1'  # Greyscale mode
        stroke_col, bg_col = (0, 1) if not is_mirrored else (1, 0)
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
