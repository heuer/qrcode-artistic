Segno PIL -- Segno plugin for creating PIL/Pillow images from QR Codes
----------------------------------------------------------------------

This `Segno <https://github.com/heuer/segno>`_ plugin converts a
(Micro) QR Code to a PIL/Pillow Image.

This plugin is not required to write PNG, EPS or PDF files. Segno's native
implementations usually generate smaller files in less time. This plugin
might be useful to modify the QR Codes (i.e. rotate or blur) or to save the
QR codes in an image format which is not supported by Segno.

Usage:

.. code-block:: python

    >>> import segno
    >>> qr = segno.make("One, two, three, four, one, two"
                        "Let me tell you how it will be"
                        "There's one for you, nineteen for me")
    >>> img = qr.to_pil()  # Greyscale image, default scale
    >>> img.save('example.png')
    >>> qr.to_pil(scale=10).show()  # Show img with scale 10
    >>> # Different scale
    >>> img = qr.to_pil(scale=3)
    >>> img.save('example-2.png')
    >>> # Different scale and change module color
    >>> img = qr.to_pil(scale=3, dark='darkblue')
    >>> img.save('example-3.png')
    >>> # Different scale and change dark and light module colors
    >>> img = qr.to_pil(scale=3, dark='#36c', light=None)
    >>> img.save('example-4.png')
    >>> # Invert the example above
    >>> img = qr.to_pil(scale=3, dark=None, light='#36c')
    >>> img.save('example-5.png')
    >>> # Save JPEG
    >>> qr.to_pil(scale=3, dark='#36c', light='yellow', mode='RGB').save('example-6.jpg')
    >>> rotated_img = pil_img.rotate(3, expand=True)
    >>> rotated_img.convert('RGB').save('example-7.jpg')
    >>> # Multiple module colors
    >>> qr = segno.make('Yellow Submarine', version=7, error='h')
    >>> img = qr.to_pil(scale=4, dark='darkred', data_dark='darkorange',
                        data_light='yellow')
    >>> img.save('yellow-submarine.png')

