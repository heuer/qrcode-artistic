Segno PIL -- Segno plugin for creating PIL/Pillow images from QR Codes
----------------------------------------------------------------------

This `Segno`_ plugin converts a (Micro) QR Code to a PIL/Pillow Image.

This plugin is not required to write PNG, EPS or PDF files. Segno's native
implementations usually generate smaller files in less time. This plugin
might be useful to modify the QR Codes (i.e. rotate or blur) or to save the
QR Codes in an image format which is not supported by Segno.

The resulting image is either a greyscale (PIL mode "1"), an indexed-color
image (PIL mode "P") or an RGBA image. The mode depends on the provided
(background) color values. The plugin chooses the optimal (minimal) mode
automatically. Use the ``mode`` parameter to enforce a specific mode. Mode "RGB"
isn't supported, though.


Usage:

.. code-block:: python

    >>> import segno
    >>> qr = segno.make('Hello world')
    >>> pil_img = qr.to_pil()  # Greyscale image, default scale
    >>> pil_img.save('example.png')
    >>> qr.to_pil(scale=10).show()  # Show img with scale 10
    >>> # Different scale
    >>> pil_img = qr.to_pil(scale=10)
    >>> pil_img.save('example-2.png')
    >>> # Different scale and change module color
    >>> pil_img = qr.to_pil(scale=10, color='darkblue')  # Indexed-color image
    >>> pil_img.save('example-3.png')
    >>> # Different scale and change module color and transparent background
    >>> pil_img = qr.to_pil(scale=10, color='#36c', background=None)
    >>> # transparency = 0 means that the first color in the palette should be
    >>> # transparent. The background color is ALWAYS the first entry in the palette
    >>> pil_img.save('example-4.png', transparency=0)
    >>> # Different scale and change module color and yellow background
    >>> # Enforce 'RGBA' mode since 'P' isn't supported by JPEG even if no color
    >>> # uses the alpha channel
    >>> qr.to_pil(scale=10, color='#36c', background='yellow', mode='RGBA').save('example-4.jpg')
    >>> rotated_img = pil_img.rotate(45, expand=True)
    >>> rotated_img.convert('RGB').save('example-5.jpg')


.. _Segno: https://github.com/heuer/segno
