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


.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/invader.png
   :width: 150px
   :align: center

This package provides a programming library and a command line interface for
conversion, creation and showing of TrueType retro fonts.


Quick start
-----------

Convert from ROM
~~~~~~~~~~~~~~~~

Download a character ROM_ (e.g., one from the MSX_) and run the following
command.

.. code:: bash

    retrofont rom2ttf -d ~/.local/share/fonts/ MSX charset_international.raw
    fc-cache -f

Open a new terminal that uses the newly created font.

.. code:: bash

    foot -f MSX

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/normal.png

The `-p` option will make the converted font the primary font. It will also
make the characters square and it will remove line spacing.

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/primary.png


Testing
~~~~~~~

The character sets can be shown using the `show` subcommand. The first (and
usually only) character set is shown as follows.

.. code:: bash

    retrofont show 0

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/show.png

Additional character sets are numbered 1, 2, etc. The primary character set
has index -1.


Creation
~~~~~~~~

Glyphs can be drawn by hand and put in a YAML file.

.. code:: yaml

    - - data:
        - ' #    # '
        - '  #  #  '
        - ' ###### '
        - '## ## ##'
        - '########'
        - ' ###### '
        - '#      #'
        - '###  ###'
        offset: 1

This file can be converted into a character ROM file, which in turn can be
used to create a TrueType font.

.. code:: bash

    retrofont yml2rom demo.yaml demo.rom
    retrofont rom2ttf -d ~/.local/share/fonts/ demo demo.rom
    fc-cache -f

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/demo.png


Modifying fonts
~~~~~~~~~~~~~~~

A character ROM file can be converted to a human readable YAML file using the
`rom2yml` subcommand, in which te glyphs can be edited. The previously shown
`yml2rom` can then be used to create the modified character ROM file.


Please see ReadTheDocs_ for the latest documentation.

.. _ROM: https://github.com/ivop/8x8-fonts
.. _MSX: https://github.com/ivop/8x8-fonts/raw/refs/heads/main/msx/charset_international.raw
.. _ReadTheDocs: https://retrofont.readthedocs.io
