Glyph tracing
=============

While bitmap fonts consist of 8-byte glyphs that themselves consist of 1-bit
encoded pixels, TrueType fonts work with outlines. To convert a bitmap font to
TrueType, a glyph needs to be traced to obtain a set of closed paths that
represent the outlines of the glyph.

Suppose we have a glyph ``b'\xff\x81\xbd\xa5\xa5\xbd\x81\xff'``, that looks as
follows.

::

    ########
    #      #
    # #### #
    # #  # #
    # #  # #
    # #### #
    #      #
    ########

The ``Tracer`` class can be used to convert this bitmap into a list of closed
paths.

.. code:: python

    from retrofont.trace import Tracer

    tracer = Tracer()
    tracer.load(b'\xff\x81\xbd\xa5\xa5\xbd\x81\xff')
    tracer.trace()
    paths = tracer.get_paths()

This produces a list of four paths, one for the outline of the large square,
one for the outline of the small square, one for the inner contours of the
small square and one for the inner contours of the large square.

.. code:: python

    print(paths[1])
    print(paths[2])

Here we see the paths of the small square. The first path is the outline, the
second one is the inner contour (hole).

.. code:: text

    [(2, 2), (2, 6), (6, 6), (6, 2)]
    [(5, 3), (5, 5), (3, 5), (3, 3)]

Notice that the outline runs clockwise, while the inner contour runs counter
clockwise. This is how outlines are distinguished from holes.
