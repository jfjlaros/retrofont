Usage
=====

.. note:: This page is outdated.

This program uses the Sharp MZ character and monitor ROMs_ for the display
character sets and the interchange character set respectively.

.. image:: images/c64_cowsay.png


``rom2ttf``
-----------

The ``rom2ttf`` subcommand creates a font that contains three character sets in the
UTF-8 Private Use Area. The interchange character set is stored at 0xe000, the
primary display character set is stored ad 0xe100 and the alternate display
character set is stored ad 0xe200. The default font is left unchanged.

.. code:: bash

    retrofont rom2ttf mz700fon.int 1z-013a.rom ~/.local/share/fonts/SharpMZ.ttf
    fc-cache -f

Open a new terminal that uses the Sharp MZ font.

::

    foot -f SharpMZ

.. image:: images/sharpmz_normal.png


The ``-p`` flag additionally changes the primary font, uses square characters
and removes line spacing.

.. code:: bash

    retrofont rom2fft mz700fon.int 1z-013a.rom ~/.local/share/fonts/SharpMZD.ttf
    fc-cache -f

Open a new terminal that uses the Sharp MZ default font.

::

    foot -f SharpMZ_P

.. image:: images/sharpmz_primary.png

.. image:: images/sharpmz_boot.png

``show``
--------

The ``show`` subcommand shows all three character sets.

::

    retrofont show

If the ``rom2ttf`` subcommand was used to create the font, the output should look as
follows.

.. image:: images/mz_normal.png

If the ``default`` subcommand was used to create the font, the output should look
as follows.

.. image:: images/default_test.png


.. _ROMs: https://ia803204.us.archive.org/view_archive.php?archive=/29/items/mame-0.221-roms-merged/mz700.zip
