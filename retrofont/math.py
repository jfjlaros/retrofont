from functools import reduce
from math import log, prod
from operator import add


def make_matrix(lst: list, dim: tuple[int, ...]) -> list[...]:
    """Make an n-dimensional matrix from a flat list.

    :arg lst: List.
    :arg dim: Dimensions of the matrix.

    :return: Matrix.
    """
    if not dim:
        return lst
    size = prod(dim)
    sdim = dim[1:]
    return [
        make_matrix(lst[i:i + size], sdim) for i in range(0, len(lst), size)]


def flatten_matrix(mtx: list[...]) -> list:
    """Make a flat list from an n-dimensional matrix.

    :arg mtx: Matrix.

    :return: List.
    """
    if not isinstance(mtx, list):
        return [mtx]
    return list(reduce(add, [flatten_matrix(s) for s in mtx], []))


def reverse_byte(byte: int) -> int:
    """Reverse the bit order in a byte.

    :arg byte: Byte.

    :return: Reversed byte.
    """
    mirrored = 0
    for i in range(8):
        mirrored <<= 1
        mirrored |= (byte >> i) & 1
    return mirrored


def pad_block(size: int, block_size: int) -> int:
    """Calculate number of padding bytes.

    :arg size: Number of bytes.
    :arg block_size: Block size.

    :return: Number of padding bytes.
    """
    bits = int(log(block_size, 2))
    return ((size - 1 >> bits) + 1 << bits) - size


def add_tuples(t1: tuple[int, int], t2: tuple[int, int]) -> tuple[int, int]:
    """Add two 2-tuples.

    :arg t1: A 2-tuple.
    :arg t2: A 2-tuple.

    :return: Result of `t1` + `t2`.
    """
    x1, y1 = t1
    x2, y2 = t2
    return (x1 + x2, y1 + y2)


def rotate_tuple_cw(t: tuple[int, int]) -> tuple[int, int]:
    """Rotate a 2-tuple 90 degrees clockwise.

    :arg t: A 2-tuple.

    :return: Rotation of `t`.
    """
    x, y = t
    return (y, -x)


def rotate_tuple_ccw(t: tuple[int, int]) -> tuple[int, int]:
    """Rotate a 2-tuple 90 degrees counterclockwise.

    :arg t: A 2-tuple.

    :return: Rotation of `t`.
    """
    x, y = t
    return (-y, x)
