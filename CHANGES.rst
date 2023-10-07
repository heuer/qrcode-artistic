Changes
=======

2.1.1 -- 2022-08-dd
-------------------
* Fixed `#11 <https://github.com/heuer/qrcode-artistic/issues/11>`_
  Providing floats for scale may result into an infinite loop;
  reported by `Abe Winter <https://github.com/abe-winter>`_
* Fixed `#5 <https://github.com/heuer/qrcode-artistic/issues/5>`_
  Added support for SVG backgrounds iff cairosvg is available;
  suggested by `Markus Ueberall <https://github.com/m-ueberall>`_
* Avoid to use deprecated Pillow constants
* Updated default Python version to 3.11 for test suite (Py 2.7 is still supported),
  added support for PyPy3 to the test suite


2.1.0 -- 2020-09-10
-------------------
* Deprecated optional "format" keyword, use "kind" for ``QRCode.to_artistic``
* Support ``io.BytesIO`` or a file-like target in ``QRCode.to_artistic``


2.0.1 -- 2020-09-04
-------------------
* Fixed `#4 <https://github.com/heuer/segno-pil/issues/4>`_:
  QR codes may be blurred if the scaling factor is greater than 3.


2.0.0 -- 2020-08-11
-------------------
* Renamed segno-pil to qrcode-artistic
* Fixed `#1 <https://github.com/heuer/segno-pil/issues/1>`_:
  Support for background images and animated QR codes.


1.0.0 -- 2020-08-07
-------------------
* Support for multiple module colors
* Support for Segno's API >= 1.0.0
* API breaking changes:

  - Changed parameter "color" to "dark" and "background" to "light" to match Segno's API
  - Removed "mode" parameter


0.1.6 -- 2016-09-19
-------------------
* Fixed Python packaging


0.1.5 -- 2016-08-24
-------------------
* Adapt Segno's 0.1.6 API changes.


0.1.4 -- 2016-08-16
-------------------
* Updated docs


0.1.3 -- 2016-08-14
-------------------
* Initial release
