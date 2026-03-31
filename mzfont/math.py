from math import log, prod


def make_matrix(l: list, dim: tuple) -> list[...]:
    """Make an n-dimensional matrix from a flat list.

    :arg l: List.
    :arg dim: Dimensions of the matrix.

    :return: Matrix.
    """
    if not dim:
        return l
    size = prod(dim)
    sdim = dim[1:]
    return [make_matrix(l[i:i + size], sdim) for i in range(0, len(l), size)]


def reverse(byte: int) -> int:
    """Reverse the bit order in a byte.

    :arg byte: Byte.

    :return: Reversed byte.
    """
    mirrored = 0
    for i in range(8):
        mirrored <<= 1
        mirrored |= (byte >> i) & 1
    return mirrored


def pad(size: int, block_size: int) -> int:
    """Calculate number of padding bytes.

    :arg size: Number of bytes.
    :arg block_size: Block size.

    :return: Number of padding bytes.
    """
    bits = int(log(block_size, 2))
    return ((size - 1 >> bits) + 1 << bits) - size
