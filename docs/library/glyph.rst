Glyph decoding, encoding and traversal
======================================

The ``glyph`` module provides several functions for encoding, decoding and
iterating over glyphs. Together, they can be used for easy glyph manipulation.

Glyphs are usually encoded in 8 bytes, each byte representing one row of the
glyph. The ``decode_glyph`` function can be used to transform a glyph to a
human readable format.

.. code:: python

    from retrofont.glyph import decode_glyph

    glyph = b'B$~\xdb\xff~\x81\xe7'
    text_glyph = decode_glyph(glyph)
    print('\n'.join(text_glyph))

The text representation of the glyph looks as follows.

::

     #    #
      #  #
     ######
    ## ## ##
    ########
     ######
    #      #
    ###  ###


This representation can easily be manipulated.

.. code:: python

    text_glyph[0] = '  #  #  '
    print('\n'.join(text_glyph))

The modified text glyph now looks as follows.

::

      #  #
      #  #
     ######
    ## ## ##
    ########
     ######
    #      #
    ###  ###


A text glyph can be encoded with ``encode_glyph`` to a glyph again.

.. code:: python

    from retrofont.glyph import encode_glyph

    glyph = encode_glyph(text_glyph)
    print(glyph)

Notice that the first byte (``$``) now differs from what we started with
(``B``).

.. code:: text

    b'$$~\xdb\xff~\x81\xe7'

Glyphs frequently need to be traversed (e.g., for printing). The
``traverse_glyph`` generator can be used for this purpose.

.. code:: python

    from retrofont.glyph import traverse_glyph

    pixels = traverse_glyph(glyph)
    for pixel in pixels:
        (r, c), v = pixel
        print(f'row: {r}, column: {c}, value: {v}')

The generator produces 2-tuples, consisting of a coordinate (also a 2-tuple)
and a value.

.. code:: text

    row: 0, column: 0, value: Pixel.empty
    row: 0, column: 1, value: Pixel.empty
    row: 0, column: 2, value: Pixel.filled
    ...
