# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 - 2023 -- Lars Heuer
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
try:
    from PIL.Image.Resampling import LANCZOS
except ImportError:
    from PIL.Image import LANCZOS
try:
    from PIL import UnidentifiedImageError
except ImportError:
    UnidentifiedImageError = IOError
_SVG_SUPPORT = False
try:
    import cairosvg
    _SVG_SUPPORT = True
except ImportError:
    pass

__version__ = '3.0.0.dev'


def write_pil(qrcode, scale=1, border=None, dark='#000', light='#fff',
              finder_dark=False, finder_light=False, data_dark=False,
              data_light=False, version_dark=False, version_light=False,
              format_dark=False, format_light=False, alignment_dark=False,
              alignment_light=False, timing_dark=False, timing_light=False,
              separator=False, dark_module=False, quiet_zone=False):
    """\
    Converts the provided `qrcode` into a Pillow image.

    If any color is ``None`` use the Image.info dict to detect which
    pixel / palette entry represents a transparent value.

    See `Colorful QR Codes <https://segno.readthedocs.io/en/stable/colorful-qrcodes.html>`_
    for a detailed description of all module colors.

    :param segno.QRCode qrcode: The QR code.
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
    qrcode.save(buff, kind='png', scale=scale, border=border, dark=dark,
                light=light, finder_dark=finder_dark, finder_light=finder_light,
                data_dark=data_dark, data_light=data_light,
                version_dark=version_dark, version_light=version_light,
                format_dark=format_dark, format_light=format_light,
                alignment_dark=alignment_dark, alignment_light=alignment_light,
                timing_dark=timing_dark, timing_light=timing_light,
                separator=separator, dark_module=dark_module, quiet_zone=quiet_zone)
    buff.seek(0)
    return Image.open(buff)


def write_artistic(qrcode, background, target, mode=None, format=None, kind=None,
                   scale=3, border=None, dark='#000', light='#fff',
                   finder_dark=False, finder_light=False, data_dark=False,
                   data_light=False, version_dark=False, version_light=False,
                   format_dark=False, format_light=False, alignment_dark=False,
                   alignment_light=False, timing_dark=False, timing_light=False,
                   separator=False, dark_module=False, quiet_zone=False):
    """\
    Saves the QR code with the background image into target.

    :param segno.QRCode qrcode: The QR code.
    :param background: Path to the background image.
    :param target: A filename or a writable file-like object with a
                    ``name`` attribute. Use the ``kind`` parameter if
                    `target` is a :py:class:`io.BytesIO` stream which does not
                    have ``name`` attribute.
    :param str mode: `Image mode <https://pillow.readthedocs.io/en/stable/handbook/concepts.html#modes>`_
    :param str kind: Optional image format (i.e. 'PNG') if the target provides no
            information about the image format.
    :param int scale: The scale. A minimum scale of 3 (default) is recommended.
            The best results are achieved with a scaling of more than 3 and a
            scaling divisible by 3. If a floating number is provided it is converted to an integer (1.5 becomes 1)
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
    scale = int(scale)
    requested_scale = scale
    while scale % 3:
        scale += 1
    qr_img = write_pil(qrcode, scale=scale, border=border, dark=dark, light=light, finder_dark=finder_dark,
                       finder_light=finder_light, data_dark=data_dark, data_light=data_light, version_dark=version_dark,
                       version_light=version_light, format_dark=format_dark, format_light=format_light,
                       alignment_dark=alignment_dark, alignment_light=alignment_light, timing_dark=timing_dark,
                       timing_light=timing_light, separator=separator, dark_module=dark_module,
                       quiet_zone=quiet_zone).convert('RGBA')
    # Maximal dimensions of the background image(s)
    # The background image is not drawn at the quiet zone of the QR Code, therefore border=0
    max_bg_width, max_bg_height = qrcode.symbol_size(scale=scale, border=0)
    if format:
        import warnings
        warnings.warn('Using format is deprecated, use "kind"', DeprecationWarning)
        kind = format
    try:
        bg_img = Image.open(background)
    except UnidentifiedImageError:
        bg_img = _svg_to_png(background, width=max_bg_width, height=max_bg_height)
    input_mode = bg_img.mode
    bg_images = [bg_img]
    is_animated = False
    if kind is None:
        try:
            fname = target.name
        except AttributeError:
            fname = target
        ext = fname[fname.rfind('.') + 1:].lower()
    else:
        ext = kind.lower()
    target_supports_animation = ext in ('gif', 'png', 'webp')
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
    border = border if border is not None else qrcode.default_border_size
    bg_width, bg_height = bg_images[0].size
    ratio = min(max_bg_width / bg_width, max_bg_height / bg_height)
    bg_width, bg_height = int(bg_width * ratio), int(bg_height * ratio)
    bg_tpl = Image.new('RGBA', (max_bg_width, max_bg_height), (255, 0, 0, 0))
    tmp_bg_images = []
    for img in (img.resize((bg_width, bg_height), LANCZOS) for img in bg_images):
        bg_img = bg_tpl.copy()
        tmp_bg_images.append(bg_img)
        pos = (int(math.ceil((max_bg_width - img.size[0]) / 2)), int(math.ceil((max_bg_height - img.size[1]) / 2)))
        bg_img.paste(img, pos)
    bg_images = tmp_bg_images
    res_images = [qr_img]
    res_images.extend([qr_img.copy()] * (len(bg_images) - 1))
    # Cache drawing functions of the result image(s)
    draw_functions = [ImageDraw.Draw(img).point for img in res_images]
    keep_modules = (consts.TYPE_FINDER_PATTERN_DARK, consts.TYPE_FINDER_PATTERN_LIGHT, consts.TYPE_SEPARATOR,
                    consts.TYPE_ALIGNMENT_PATTERN_DARK, consts.TYPE_ALIGNMENT_PATTERN_LIGHT, consts.TYPE_TIMING_DARK,
                    consts.TYPE_TIMING_LIGHT)
    border_offset = border * scale
    d = scale // 3
    for i, row in enumerate(qrcode.matrix_iter(scale=scale, border=0, verbose=True)):
        for j, m in enumerate(row):
            if m in keep_modules:
                continue
            if not (((i // d) % 3 == 1) and ((j // d) % 3 == 1)):
                for img_idx, img in enumerate(bg_images):
                    fill = img.getpixel((i, j))
                    if fill[3]:
                        draw_functions[img_idx]((i + border_offset, j + border_offset), fill)
    if scale != requested_scale:
        bg_width, bg_height = max_bg_width, max_bg_height
        max_bg_width, max_bg_height = qrcode.symbol_size(scale=requested_scale, border=border)
        ratio = min(max_bg_width / bg_width, max_bg_height / bg_height)
        bg_width, bg_height = int(bg_width * ratio), int(bg_height * ratio)
        res_images = [img.resize((bg_width, bg_height), LANCZOS) for img in res_images]
    if mode is None and input_mode != 'RGBA':
        res_images = [img.convert(input_mode) for img in res_images]
    elif mode is not None:
        res_images = [img.convert(mode) for img in res_images]
    if is_animated:
        res_images[0].save(target, format=kind, uration=durations, save_all=True, append_images=res_images[1:],
                           loop=loop)
    else:
        res_images[0].save(target, format=kind)


def _svg_to_png(source, width, height):
    """\
    Converts the SVG source into a PNG and returns a PIL.Image

    :param source: The SVG source.
    :param width: The target width.
    :param height: The target height.
    :return: Image.
    """
    out = io.BytesIO()
    try:
        source.name
    except AttributeError:
        pass
    with open(source, 'rb') as f:
        cairosvg.svg2png(file_obj=f, write_to=out)
    out.seek(0)
    img = Image.open(out)
    svg_width, svg_height = img.size
    ratio = min(width / svg_width, height / svg_height)
    w, h = int(svg_width * ratio), int(svg_height * ratio)
    out = io.BytesIO()
    with open(source, 'rb') as f:
        cairosvg.svg2png(file_obj=f, write_to=out, output_width=w, output_height=h)
    out.seek(0)
    return Image.open(out)


if not _SVG_SUPPORT:
    def _svg_to_png(source, width=None, height=None):  # noqa: F811
        raise ValueError('cairosvg is required for SVG support')
