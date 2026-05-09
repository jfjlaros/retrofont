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

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/UFO.png

This package provides a way to generate and test TrueType retro fonts.


Quick start
-----------

Download the Sharp MZ character and monitor ROMs_ and run the following
command.

.. code:: bash

    retrofont make mz700fon.int 1z-013a.rom ~/.local/share/fonts/SharpMZ.ttf
    fc-cache -fv ~/.local/share/fonts

Open a new terminal that uses the Sharp MZ font.

::

    foot -f SharpMZ

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/normal_font.png

The `default` subcommand additionally changes the default font, uses square
characters and removes line spacing.

.. image:: https://raw.githubusercontent.com/jfjlaros/retrofont/master/docs/images/default_font.png

Please see ReadTheDocs_ for the latest documentation.


.. _ROMs: https://ia803204.us.archive.org/view_archive.php?archive=/29/items/mame-0.221-roms-merged/mz700.zip
.. _ReadTheDocs: https://retrofont.readthedocs.io
