Artistic QR Codes
-----------------

This `Segno <https://github.com/heuer/segno>`_ plugin converts a
(Micro) QR Code to a Pillow Image or into a QR code with a background
image.

This plugin is not required to write PNG, EPS or PDF files. Segno's native
implementations usually generate smaller files in less time.

This plugin might be useful to modify the QR Codes (i.e. rotate or blur)
or to save the QR codes in an image format which is not supported by Segno.

Furthermore, QR codes can be created with a background image.

.. image:: https://github.com/heuer/qrcode-artistic/raw/master/images/beatles.jpg

.. image:: https://github.com/heuer/qrcode-artistic/raw/master/images/beatles-animated.gif


Transparency is supported as well

.. image:: https://github.com/heuer/qrcode-artistic/raw/master/images/maggie.gif


Use ``pip`` to install from PyPI::

    $ pip install qrcode-artistic


Documentation: https://segno.readthedocs.io/en/latest/artistic-qrcodes.html
