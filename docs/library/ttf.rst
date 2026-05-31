TrueType font generation
========================

The ``TTF`` class can be used to add character sets to existing fonts and to
modify the primary character set of an existing font.

.. code:: python

    from retrofont.ttf import TTF

    base_font = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
    font_name = 'myFont'
    ttf = TTF(base_font, font_name)

The ``add_charset`` method is used to add a character set to the font.

.. code:: python

    from retrofont.font import rom_to_font

    data = open('data/test_font.rom', 'rb').read()
    font = rom_to_font(data)
    for charset in font:
        ttf.add_charset(charset)

The ``make_font`` method writes the font to a file. The class instance cannot
be used after calling this method.

.. code:: python

    ttf.make_font('myFont.ttf')
