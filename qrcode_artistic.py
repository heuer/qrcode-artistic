# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2020 -- Lars Heuer
# All rights reserved.
#
# License: BSD License
#
"""\
Segno writer plugin to convert a (Micro) QR code into a Pillow Image and
and to add (animated) background images to QR codes.
"""
from __future__ import absolute_import, unicode_literals, division
import io
import math
from PIL import Image, ImageDraw, ImageSequence
from segno import consts

__version__ = '2.0.0'


def write_pil(qrcode, scale=1, border=None, dark='#000', light='#fff',
              finder_dark=False, finder_light=False,
              data_dark=False, data_light=False,
              version_dark=False, version_light=False,
              format_dark=False, format_light=False,
              alignment_dark=False, alignment_light=False,
              timing_dark=False, timing_light=False,
              separator=False, dark_module=False, quiet_zone=False):
    """\
    Converts the provided `qrcode` into a Pillow image.

    If any color is ``None`` use the Image.info dict to detect which
    pixel / palette entry represents a transparent value.

    See `Colorful QR Codes <https://segno.readthedocs.io/en/stable/colorful-qrcodes.html>`_
    for a detailed description of all module colors.

    :param scale: Indicates the size of a single module (default: 1 which
            corresponds to 1 x 1 pixel per module).
    :param border: Integer indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for Micro QR Codes).
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
    # Cheating here ;) Let Segno write a PNG image and open it with Pillow
    # Versions < 1.0.0 used Pillow to draw the QR code but there was no benefit,
    # just duplicate code
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


def write_artistic(qrcode, background, target, mode=None, format=None,
                   scale=3, border=None, dark='#000', light='#fff',
                   finder_dark=False, finder_light=False,
                   data_dark=False, data_light=False,
                   version_dark=False, version_light=False,
                   format_dark=False, format_light=False,
                   alignment_dark=False, alignment_light=False,
                   timing_dark=False, timing_light=False,
                   separator=False, dark_module=False, quiet_zone=False):
    """\
    Saves the QR code with the background image into target.

    :param background: Path to the background image.
    :param target: Path to the target image.
    :param str mode: `Image mode <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes>`_
    :param str format: Optional image format (i.e. 'PNG') if the target provides no
                       information about the image format.
    :param scale: The scale. A minimum scale of 3 (default) is recommended.
    :param int border: Number indicating the size of the quiet zone.
            If set to ``None`` (default), the recommended border size
            will be used (``4`` for QR Codes, ``2`` for Micro QR Codes).
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
    qr_img = write_pil(qrcode, scale=3, border=border, dark=dark, light=light,
                       finder_dark=finder_dark, finder_light=finder_light,
                       data_dark=data_dark, data_light=data_light,
                       version_dark=version_dark, version_light=version_light,
                       format_dark=format_dark, format_light=format_light,
                       alignment_dark=alignment_dark, alignment_light=alignment_light,
                       timing_dark=timing_dark, timing_light=timing_light,
                       separator=separator, dark_module=dark_module,
                       quiet_zone=quiet_zone).convert('RGBA')
    bg_img = Image.open(background)
    input_mode = bg_img.mode
    bg_images = [bg_img]
    is_animated = False
    target_supports_animation = target[target.rindex('.') + 1:] in ('gif', 'png', 'webp')
    try:
        is_animated = target_supports_animation and bg_img.is_animated
    except AttributeError:
        pass
    durations = None
    loop = 0
    if is_animated:
        loop = bg_img.info.get('loop', 0)
        bg_images.extend([frame.copy() for frame in ImageSequence.Iterator(bg_img)])
        durations = [img.info.get('duration', 0) for img in bg_images]
    border = border if border else (2 if qrcode.is_micro else 4)
    # Maximal dimensions of the background image(s)
    # The background image is not drawn at the quiet zone of the QR Code, therefore border=0
    max_bg_width, max_bg_height = qrcode.symbol_size(scale=3, border=0)
    bg_width, bg_height = bg_images[0].size
    ratio = min(max_bg_width / bg_width, max_bg_height / bg_height)
    bg_width, bg_height = int(bg_width * ratio), int(bg_height * ratio)
    bg_tpl = Image.new('RGBA', (max_bg_width, max_bg_height), (255, 0, 0, 0))
    tmp_bg_images = []
    for img in (img.resize((bg_width, bg_height), Image.LANCZOS) for img in bg_images):
        bg_img = bg_tpl.copy()
        tmp_bg_images.append(bg_img)
        pos = int(math.ceil((max_bg_width - img.size[0]) / 2)), int(math.ceil((max_bg_height - img.size[1]) / 2))
        bg_img.paste(img, pos)
    bg_images = tmp_bg_images
    res_images = [qr_img]
    res_images.extend([qr_img.copy() for i in range(len(bg_images) - 1)])
    # Cache drawing functions of the result image(s)
    draw_functions = [ImageDraw.Draw(img).point for img in res_images]
    border_offset = border * 3
    keep_modules = [consts.TYPE_FINDER_PATTERN_DARK, consts.TYPE_FINDER_PATTERN_LIGHT, consts.TYPE_SEPARATOR,
                    consts.TYPE_ALIGNMENT_PATTERN_DARK, consts.TYPE_ALIGNMENT_PATTERN_LIGHT,
                    consts.TYPE_TIMING_DARK, consts.TYPE_TIMING_LIGHT]
    for i, row in enumerate(qrcode.matrix_iter(scale=3, border=0, verbose=True)):
        for j, bit in enumerate(row):
            if bit in keep_modules:
                continue
            if not (i % 3 == 1 and j % 3 == 1):
                for img_idx, img in enumerate(bg_images):
                    fill = img.getpixel((i, j))
                    if fill[3]:
                        draw_functions[img_idx]((i + border_offset, j + border_offset), fill)
    if scale != 3:
        bg_width, bg_height = max_bg_width, max_bg_height
        max_bg_width, max_bg_height = qrcode.symbol_size(scale=scale, border=border)
        ratio = min(max_bg_width / bg_width, max_bg_height / bg_height)
        bg_width, bg_height = int(bg_width * ratio), int(bg_height * ratio)
        res_images = [img.resize((bg_width, bg_height), Image.LANCZOS) for img in res_images]
    if mode is None and input_mode != 'RGBA':
        res_images = [img.convert(input_mode) for img in res_images]
    elif mode is not None:
        res_images = [img.convert(mode) for img in res_images]
    if is_animated:
        res_images[0].save(target, format=format,
                           duration=durations, save_all=True,
                           append_images=res_images[1:], loop=loop)
    else:
        res_images[0].save(target, format=format)
