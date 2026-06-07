Font conversions and manipulation
=================================

A font can be loaded from a ROM image using the ``rom_to_font`` function.

.. code:: python

    from retrofont.font import rom_to_font

    data = open('data/test_font.rom', 'rb').read()
    font = rom_to_font(data)
    print('Number of character sets:', len(font))
    print('Size of a character set:', len(font[0]))

This particular font contains three character sets, each containing 256
glyphs.

.. code:: text

    Number of character sets: 3
    Size of a character set: 256


A font can be converted back to a ROM image using the ``font_to_rom``
function.

.. code:: python

    from retrofont.font import font_to_rom

    data = font_to_rom(font)
    print('Size of the ROM image:', len(data))

The serialised ROM image size for this particular font is 6144 bytes.

.. code:: text

    Size of the ROM image: 6144

A text font can be loaded from a YAML file.

.. code:: python

    from yaml import safe_load

    text_font = safe_load(open('data/test_font.yaml', 'rt'))
    print('Size of the first character set:', len(text_font[0]))

A text font does not contain any empty glyphs. The first character set in this
particular font contains two glyphs.

.. code:: text

    Size of the first character set: 2

A text glyph consists of a ``data`` field, containing a text representation of
the glyph and an ``offset`` field, denoting the position of the glyph in the
character set.

.. code:: python

    from pprint import PrettyPrinter
    pp = PrettyPrinter(indent=2)
    pp.pprint(text_font[0][0])

The first non-empty glyph in the first character set of this font, happens to
be an 'A' that is positioned at offset 65.

.. code:: python

    { 'data': [ ' #####  ',
                '#     # ',
                '#     # ',
                '####### ',
                '#     # ',
                '#     # ',
                '#     # ',
                '        '],
      'offset': 65}

Text fonts can be converted to a normal (binary) font using the
``yaml_to_font`` function.

.. code:: python

    from retrofont.font import yaml_to_font

    font = yaml_to_font(text_font)
    print('Size of the first character set:', len(font[0]))

The first character set of this font contains 256 glyphs instead of the two we
found in the text font. Any undefined glyphs have been converted to the empty
glyph.

.. code:: text

    Size of the first character set: 256

Vice versa, fonts can be converted to YAML using the ``font_to_yaml``
function.

.. code:: python

    from retrofont.font import font_to_yaml

    text_font = font_to_yaml(font)
    print('Size of the first character set:', len(text_font[0]))

Notice that the empty characters are no longer present in the text font.

.. code:: text

    Size of the first character set: 2

ROM images do not necessarily contain all glyphs in the same order as they are
used. This is particularly noticeable when using a bitmap font as primary
font. If the glyphs are not at their standard ASCII position, the terminal may
become unusable. This is why system specific configurations are available.

.. code:: python

    from retrofont.config import read_config, select_system_config

    config = read_config()
    system_config = select_system_config(config['systems'], 'C64')
    pp.pprint(system_config)


.. code:: python

    { 'name': 'C64',
      'primary': { 'character_blocks': [[32, [32, 96]], [96, [0, 32]]],
                   'characters': [[64, 0], [95, 100], [124, 93]]}}

See the :ref:`config_system` section for more information about system
configuration.

These mappings are converted to a permutation using the
``keymap_to_permutation`` function.

.. code:: python

    from retrofont.font import keymap_to_permutation

    permutation = keymap_to_permutation(system_config['primary'])
    print('Character 32 is at position', permutation[32], 'in the ROM image')
    print('Character 97 is at position', permutation[97], 'in the ROM image')
    print('Character 64 is at position', permutation[64], 'in the ROM image')

The provided mappings are now in a flat permutation list.

.. code:: text

    Character 32 is at position 32 in the ROM image
    Character 97 is at position 1 in the ROM image
    Character 64 is at position 0 in the ROM image

A permutation can be used to map a character set using the ``map_charset``
function.

.. code:: python

    from retrofont.font import map_charset

    new_charset = map_charset(font[0], permutation)
    print(new_charset[97] == font[0][1])

Similarly, the permutation can be applied to every character set in the font
using the `map_font` function.

.. code:: python

    from retrofont.font import map_font

    new_font = map_font(font, permutation)
    print(new_font[0][97] == font[0][1])
