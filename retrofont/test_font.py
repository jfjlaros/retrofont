from sys import stdout


def print_charset(charset: int) -> None:
    '''Print a character set.

    :arg offset: Character set offset relative to 0xe000.
    '''
    offset = 0xe000 + 0x100 * charset

    stdout.write('  | ' + ' '.join([f'{i:x}' for i in range(0x10)]) + '\n')
    stdout.write(f'--+{"--" * 0x10}\n')
    for i in range(0x10):
        stdout.write(f'{i:x} |')
        for j in range(0x10):
            stdout.write(f' {chr(offset + (i << 4 | j))}')
        stdout.write('\n')
