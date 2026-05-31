Configuration
=============

RetroFont uses a configuration file for:

- Specifying the base font.
- Primary font mapping.
- Glyph mirroring.
- Character set mapping.

The package includes a configuration file, the location of which is shown by
the following command.

::

    retrofont show_config

To modify the configuration, a copy can be placed in the user's home
directory.

.. code:: text

    mkdir -p ~/.config/retrofont/
    cp $(retrofont show_config) ~/.config/retrofont/config.yaml

This new configuration file will now be used instead of the one provided in
the package.


Base font
---------

To change the base font, the ``base`` variable in the ``font`` section should
be set to the file name of a TrueType font. Make sure this is a monospaced
font.


Systems
-------

How to add a system.

- Mirroring glyphs.
- Mapping character sets.
- Character blocks.
- Single characters.


Contributing
------------

Additions are welcome [link to contributing].
