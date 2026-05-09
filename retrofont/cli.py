from argparse import RawDescriptionHelpFormatter, ArgumentParser, FileType
from os.path import expanduser
from typing import BinaryIO

from . import doc_split
from .charset import (
    map_charset, map_charsets, read_keymap, read_map, read_rom)
from .config import read_config, select_system
from .font import Font
from .meta import _copyright, _description, _info
from .font import Font
from .test_font import print_charset


def make_font(
        name: str, cgrom: BinaryIO, fwrom: BinaryIO=None, sys_type: str='',
        dest: str='.', primary: bool=False) -> None:
    """Create a TrueType font.

    :arg name: Font name.
    :arg gcrom: Character ROM file.
    :arg fwrom: Firmware ROM file.
    :arg sys_type: System type.
    :arg dest: Destination directory.
    :art primary: Generate primary font.
    """
    config = read_config()
    system = select_system(config['systems'], sys_type)
    charsets = read_rom(cgrom, mirror=system.get('mirror', False))

    font = Font(config['font']['base'], name)
    if primary:
        font.config_primary()
        keymap = system.get('primary', {})
        primary_charset = map_charset(charsets[0], read_keymap(keymap))
        font.set_primary(primary_charset)

    if fwrom:
        permutation = read_map(fwrom, system.get('map_offset', 0))
        permuted = map_charsets(charsets, permutation)
        for charset in permuted:
            font.add_charset(charset)

    for charset in charsets:
        font.add_charset(charset)

    font.make_font(expanduser(f'{dest}/{name}.ttf'))


def _arg_parser():
    parser = ArgumentParser(
        description = _description, epilog=_copyright,
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        '-v', action='version', version=_info)
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    make_font_parser = subparsers.add_parser(
        'make', description=doc_split(make_font))
    make_font_parser.add_argument(
        'name', metavar='NAME', type=str, help='font name')
    make_font_parser.add_argument(
        'cgrom', metavar='CGROM', type=FileType('rb'),
        help='character ROM file')
    make_font_parser.add_argument(
        '-f', dest='fwrom', type=FileType('rb'), default=None,
        help='firmware ROM file')
    make_font_parser.add_argument(
        '-s', dest='sys_type', type=str, default='',
        help='system name')
    make_font_parser.add_argument(
        '-d', dest='dest', type=str, default='.',
        help='destination directory')
    make_font_parser.add_argument(
        '-p', dest='primary', default=False, action='store_true',
        help='generate primary font')
    make_font_parser.set_defaults(func=make_font)

    test_font_parser = subparsers.add_parser(
        'test', description=doc_split(print_charset))
    test_font_parser.add_argument(
        'charset', metavar='CHARSET', type=int,
        help='character set')
    test_font_parser.set_defaults(func=print_charset)

    return parser


def main():
    parser = _arg_parser()

    try:
        args = parser.parse_args()
    except IOError as error:
        parser.error(error)

    try:
        args.func(**{
            k: v for k, v in vars(args).items()
            if k not in ('func', 'subcommand')})
    except ValueError as error:
        parser.error(error)
