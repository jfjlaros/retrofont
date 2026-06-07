RetroFont: TrueType font generator
==================================

.. image:: https://img.shields.io/github/last-commit/jfjlaros/retrofont.svg
   :target: https://github.com/jfjlaros/retrofont/graphs/commit-activity
.. image:: https://readthedocs.org/projects/retrofont/badge/?version=latest
   :target: https://retrofont.readthedocs.io/en/latest
.. image:: https://img.shields.io/github/release-date/jfjlaros/retrofont.svg
   :target: https://github.com/jfjlaros/retrofont/releases
.. image:: https://img.shields.io/github/release/jfjlaros/retrofont.svg
   :target: https://github.com/jfjlaros/retrofont/releases
.. image:: https://img.shields.io/pypi/v/retrofont.svg
   :target: https://pypi.org/project/retrofont/
.. image:: https://img.shields.io/github/languages/code-size/jfjlaros/retrofont.svg
   :target: https://github.com/jfjlaros/retrofont
.. image:: https://img.shields.io/github/languages/count/jfjlaros/retrofont.svg
   :target: https://github.com/jfjlaros/retrofont
.. image:: https://img.shields.io/github/languages/top/jfjlaros/retrofont.svg
   :target: https://github.com/jfjlaros/retrofont
.. image:: https://img.shields.io/github/license/jfjlaros/retrofont.svg
   :target: https://raw.githubusercontent.com/jfjlaros/retrofont/master/LICENSE.md

----

This package provides a programming library and a command line interface for
conversion, creation and manipulation of TrueType retro fonts.

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/invader.png
   :width: 150px
   :align: center


.. _quickstart:

Quick start
-----------

Convert from ROM
~~~~~~~~~~~~~~~~

Download a character ROM_ (e.g., one from the MSX_) and run the following
command.

.. code:: text

    retrofont rom2ttf -d ~/.local/share/fonts/ MSX charset_international.raw
    fc-cache -f

Open a new terminal that uses the newly created font. In Wayland we can use
``foot`` as follows.

.. code:: text

    foot -f MSX

In X, we can use ``xterm``.

.. code:: text

    xterm -fa MSX

.. figure:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/msx_normal.png

    Plain text mixed with MSX characters.

The ``-p`` option additionally uses the converted font as the primary font. It
will also make the characters square and it will remove line spacing.

.. figure:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/msx_primary.png

    Primary font using the MSX character set.

Adjusting the terminal foreground and background colours can have quite a
convincing effect.

.. figure:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/c64_boot.png

    Not a screenshot of a Commodore 64 emulator.


Creation
~~~~~~~~

Glyphs can be drawn by hand and put in a YAML file.

.. code:: yaml

    - # ...
    - - data:
        - ' #    # '
        - '  #  #  '
        - ' ###### '
        - '## ## ##'
        - '########'
        - ' ###### '
        - '#      #'
        - '###  ###'
        offset: 0
      # ...

This file can be converted into a character ROM file, which in turn can be
used to create a TrueType font.

.. code:: text

    retrofont yml2rom test_font.yaml test_font.rom
    retrofont rom2ttf -d ~/.local/share/fonts/ test_font test_font.rom
    fc-cache -f

.. figure:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/test_font.png

    Newly created glyph in the UTF-8 Private Use Area.


Please see ReadTheDocs_ for the latest documentation.


.. _ROM: https://github.com/ivop/8x8-fonts
.. _MSX: https://github.com/ivop/8x8-fonts/raw/refs/heads/main/msx/charset_international.raw
.. _ReadTheDocs: https://retrofont.readthedocs.io
