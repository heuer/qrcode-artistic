Segno PIL -- Segno plugin for creating PIL/Pillow images from QR Codes
----------------------------------------------------------------------

This `Segno`_ plugin converts a (Micro) QR Code to a PIL/Pillow Image.

This plugin is not required to write PNG files. If you want to create a PNG
file, it's recommended to use Segno's native ``png`` method.

The resulting image is either a greyscale (PIL mode "1") or an indexed-color
image (PIL mode "P"). The latter is generated if the module color is not black
or the background color is not white (i.e. transparent or any other color).


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
    >>> pil_img.save('example-4.png', transparency=0)
    >>> # Different scale and change module color and yellow background
    >>> pil_img = qr.to_pil(scale=10, color='#36c', background='yellow')
    >>> pil_img.convert('RGB').save('example-4.jpg')  # Save as JPEG (does not support "P" images)
    >>> rotated_img = pil_img.rotate(45, expand=True)
    >>> rotated_img.convert('RGB').save('example-5.jpg')


.. _Segno: https://github.com/heuer/segno
