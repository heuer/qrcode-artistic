# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Segno writer plugin to convert a (Micro) QR Code into a PIL/Pillow Image.
"""
from __future__ import absolute_import
import io
try:
    from PIL import Image
except ImportError:  # pragma: no cover
    try:
        import Image
    except ImportError:  # pragma: no cover
        import warnings
        warnings.warn('PIL or Pillow is required')
        raise

__version__ = '1.0.1.dev0'


def write_pil(qrcode, scale=1, border=None, dark='#000', light='#fff',
              finder_dark=False, finder_light=False,
              data_dark=False, data_light=False,
              version_dark=False, version_light=False,
              format_dark=False, format_light=False,
              alignment_dark=False, alignment_light=False,
              timing_dark=False, timing_light=False,
              separator=False, dark_module=False, quiet_zone=False):
    """\
    Converts the provided `qrcode` into a PIL/Pillow image.

    If any color is ``None`` use the Image.info dict to detect which
    pixel / palette entry represents a transparent value.

    See `Colorful QR Codes <https://segno.readthedocs.io/en/stable/colorful-qrcodes.html>`_
    for a detailed description of all module colors.

    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for a Micro QR Codes).
    :param dark: Color of the dark modules (default: black). The
            color can be provided as ``(R, G, B)`` tuple, as hexadecimal
            format (``#RGB``, ``#RRGGBB`` ``RRGGBBAA``), or web color
            name (i.e. ``red``).
    :param light: Color of the light modules (default: white).
            See `color` for valid values. If light is set to ``None`` the
            light modules will be transparent.
    :param finder_dark: Color of the dark finder modules (default: same as ``dark``)
    :param finder_light: Color of the light finder modules (default: same as ``light``)
    :param data_dark: Color of the dark data modules (default: same as ``dark``)
    :param data_light: Color of the light data modules (default: same as ``light``)
    :param version_dark: Color of the dark version modules (default: same as ``dark``)
    :param version_light: Color of the light version modules (default: same as ``light``)
    :param format_dark: Color of the dark format modules (default: same as ``dark``)
    :param format_light: Color of the light format modules (default: same as ``light``)
    :param alignment_dark: Color of the dark alignment modules (default: same as ``dark``)
    :param alignment_light: Color of the light alignment modules (default: same as ``light``)
    :param timing_dark: Color of the dark timing pattern modules (default: same as ``dark``)
    :param timing_light: Color of the light timing pattern modules (default: same as ``light``)
    :param separator: Color of the separator (default: same as ``light``)
    :param dark_module: Color of the dark module (default: same as ``dark``)
    :param quiet_zone: Color of the quiet zone modules (default: same as ``light``)
    """
    buff = io.BytesIO()
    qrcode.save(buff, kind='png', scale=scale, border=border, dark=dark, light=light,
                finder_dark=finder_dark, finder_light=finder_light,
                data_dark=data_dark, data_light=data_light,
                version_dark=version_dark, version_light=version_light,
                format_dark=format_dark, format_light=format_light,
                alignment_dark=alignment_dark, alignment_light=alignment_light,
                timing_dark=timing_dark, timing_light=timing_light,
                separator=separator, dark_module=dark_module, quiet_zone=quiet_zone)
    buff.seek(0)
    return Image.open(buff)
