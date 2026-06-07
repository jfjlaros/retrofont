from retrofont.math import (
    make_matrix, flatten_matrix, reverse_byte, pad_block, add_tuples,
    rotate_tuple_cw, rotate_tuple_ccw)


def test_make_matrix():
    lst = [1, 2, 3, 4]

    assert make_matrix(lst, ()) == [1, 2, 3, 4]
    assert make_matrix(lst, (1,)) == [[1], [2], [3], [4]]
    assert make_matrix(lst, (2,)) == [[1, 2], [3, 4]]
    assert make_matrix(lst, (2, 1)) == [[[1], [2]], [[3], [4]]]


def test_flatten_matrix():
    lst = [1, 2, 3, 4]

    assert flatten_matrix([1, 2, 3, 4]) == lst
    assert flatten_matrix([[1], [2], [3], [4]]) == lst
    assert flatten_matrix([[1, 2], [3, 4]]) == lst
    assert flatten_matrix([[[1], [2]], [[3], [4]]]) == lst
    assert flatten_matrix([[[1], [2]], [[3], [4]], []]) == lst


def test_reverse_byte():
    assert reverse_byte(0b01101001) == 0b10010110
    assert reverse_byte(0b11100000) == 0b00000111


def test_pad_block():
    assert pad_block(15, 8) == 1
    assert pad_block(16, 8) == 0
    assert pad_block(17, 8) == 7


def test_add_tuples():
    assert add_tuples((1, 2), (3, 4)) == (4, 6)


def test_rotate_tuple_cw():
    assert rotate_tuple_cw((0, 1)) == (1, 0)
    assert rotate_tuple_cw((1, 0)) == (0, -1)
    assert rotate_tuple_cw((0, -1)) == (-1, 0)
    assert rotate_tuple_cw((-1, 0)) == (0, 1)


def test_rotate_tuple_ccw():
    assert rotate_tuple_ccw((0, 1)) == (-1, 0)
    assert rotate_tuple_ccw((-1, 0)) == (0, -1)
    assert rotate_tuple_ccw((0, -1)) == (1, 0)
    assert rotate_tuple_ccw((1, 0)) == (0, 1)
