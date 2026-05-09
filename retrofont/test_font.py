from sys import stdout


def _printable(character: int) -> None:
    if character < 0x20:
        return ' '
    return chr(character)


def _print_charset(offset: int) -> None:
    stdout.write('  | ' + ' '.join([f'{i:x}' for i in range(0x10)]) + '\n')
    stdout.write(f'--+{"--" * 0x10}\n')
    for i in range(0x10):
        stdout.write(f'{i:x} |')
        for j in range(0x10):
            stdout.write(f' {_printable(offset + (i << 4 | j))}')
        stdout.write('\n')


def print_charset(charset: int) -> None:
    """Print a character set.

    :arg charset: Character set number.
    """
    if (charset == -1):
        _print_charset(0)
        return
    _print_charset(0xe000 + 0x100 * charset)
