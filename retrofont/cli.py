from argparse import RawDescriptionHelpFormatter, ArgumentParser, FileType
from os.path import expanduser
from sys import stdout
from typing import BinaryIO, TextIO
from yaml import safe_dump, safe_load

from . import doc_split
from .font import (
    map_charset, map_font, keymap_to_permutation, rom_to_font, visualise,
    yaml_to_font, font_to_yaml, font_to_rom)
from .config import read_config, select_system
from .ttf import TTF
from .meta import _copyright, _description, _info


def rom2ttf(
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
    font = rom_to_font(cgrom.read(), mirror=system.get('mirror', False))

    ttf = TTF(config['font']['base'], name)
    if primary:
        ttf.config_primary()
        keymap = system.get('primary', {})
        primary_charset = map_charset(font[0], keymap_to_permutation(keymap))
        ttf.set_primary(primary_charset)

    if fwrom:
        offset = system.get('map_offset', 0)
        permutation = fwrom.read()[offset:offset + 256]
        permuted = map_font(font, permutation)
        for charset in permuted:
            ttf.add_charset(charset)

    for charset in font:
        ttf.add_charset(charset)

    ttf.make_font(expanduser(f'{dest}/{name}.ttf'))


def yml2rom(text_handle: TextIO, binary_handle: BinaryIO) -> None:
    """
    """
    font = yaml_to_font(safe_load(text_handle))
    binary_handle.write(font_to_rom(font))


def rom2yml(binary_handle: BinaryIO, text_handle: TextIO) -> None:
    """
    """
    font = rom_to_font(binary_handle.read())
    text_handle.write(safe_dump(font_to_yaml(font)))


def show_charset(handle: TextIO, charset: int) -> None:
    """Print a character set.

    :arg handle: Handle to output text stream.
    :arg charset: Character set number.
    """
    offset = 0xe000 + 0x100 * charset if charset != -1 else 0
    handle.write('\n'.join(visualise(offset)) + '\n')


def _arg_parser():
    parser = ArgumentParser(
        description = _description, epilog=_copyright,
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        '-v', action='version', version=_info)
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    rom2ttf_parser = subparsers.add_parser(
        'rom2ttf', description=doc_split(rom2ttf))
    rom2ttf_parser.add_argument(
        '-d', dest='dest', type=str, default='.',
        help='destination directory')
    rom2ttf_parser.add_argument(
        '-f', dest='fwrom', type=FileType('rb'), default=None,
        help='firmware ROM file')
    rom2ttf_parser.add_argument(
        '-s', dest='sys_type', type=str, default='',
        help='system name')
    rom2ttf_parser.add_argument(
        '-p', dest='primary', default=False, action='store_true',
        help='generate primary font')
    rom2ttf_parser.add_argument(
        'name', metavar='NAME', type=str, help='font name')
    rom2ttf_parser.add_argument(
        'cgrom', metavar='CGROM', type=FileType('rb'),
        help='character ROM file')
    rom2ttf_parser.set_defaults(func=rom2ttf)

    yml2rom_parser = subparsers.add_parser(
        'yml2rom', description=doc_split(yml2rom))
    yml2rom_parser.add_argument(
        'text_handle', metavar='GLYPHS', type=FileType('rt'),
        help='glyphs in YAML format')
    yml2rom_parser.add_argument(
        'binary_handle', metavar='CGROM', type=FileType('wb'),
        help='character ROM file')
    yml2rom_parser.set_defaults(func=yml2rom)

    rom2yml_parser = subparsers.add_parser(
        'rom2yml', description=doc_split(rom2yml))
    rom2yml_parser.add_argument(
        'binary_handle', metavar='CGROM', type=FileType('rb'),
        help='character ROM file')
    rom2yml_parser.add_argument(
        'text_handle', metavar='GLYPHS', type=FileType('wt'),
        help='glyphs in YAML format')
    rom2yml_parser.set_defaults(func=rom2yml)

    show_font_parser = subparsers.add_parser(
        'show', description=doc_split(show_charset))
    show_font_parser.add_argument(
        'charset', metavar='CHARSET', type=int,
        help='character set')
    show_font_parser.add_argument(
        '-o', dest='handle', type=FileType('wt'), default=stdout,
        help='output file')
    show_font_parser.set_defaults(func=show_charset)

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
