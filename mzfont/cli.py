from argparse import RawDescriptionHelpFormatter, ArgumentParser, FileType
from importlib import resources
from sys import stdout
from yaml import safe_load

from . import doc_split
from .meta import _copyright, _description, _info
from .make_font import Font
from .test_font import print_charsets


def _parse_config():
    config_file = resources.files() / 'config.yaml'
    with config_file.open("rt") as config:
        return safe_load(config.read())


def _get_system(systems, name):
    for system in systems:
        if system['name'] == name:
            return system
    raise ValueError(f'System "{name}" not supported.')


def systems():
    """ Show supported systems."""
    supported_systems = [sys['name'] for sys in _parse_config()['systems']]
    stdout.write(f'Supported systems: {', '.join(supported_systems)}\n')


def make_font(system, glyphs_handle, firmware_handle, base_font, ttf_font):
    config = _parse_config()
    system = _get_system(config['systems'], system)
    font = base_font or config['font']['base']

    if 'map_offset' in system and not firmware_handle:
        raise ValueError('Firmware needed for this system, use `-f`.')
    font = Font(
        glyphs_handle, firmware_handle,
        system.get('map_offset', 0), system.get('mirror', False), font, system['name'])
    for i, charset in enumerate(system['sets']):
        font.make_charset(
            0xe000 + 0x100 * i, charset['location'], charset.get('map', False))
    font.make_font(ttf_font)


def make_default_font(
        glyphs_handle, perm_handle, base_font, ttf_font, font_name):
    mzfont = Font(glyphs_handle, perm_handle, base_font, font_name)
    mzfont.make_default_font(ttf_font)


def _arg_parser():
    make_parser = ArgumentParser(add_help=False)
    make_parser.add_argument(
        'system', metavar='SYSTEM', type=str, help='system name')
    make_parser.add_argument(
        'glyphs_handle', metavar='CG', type=FileType('rb'),
        help='character rom file')
    make_parser.add_argument(
        'ttf_font', metavar='TTF', type=str,
        help='output file')
    make_parser.add_argument(
        '-f', dest='firmware_handle', type=FileType('rb'), default=None,
        help='firmware rom file')
    make_parser.add_argument(
        '-b', dest='base_font', metavar='BASE', type=str, default='',
        help='base font file')

    parser = ArgumentParser(
        description = _description, epilog=_copyright,
        formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument(
        '-v', action='version', version=_info)
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True

    make_font_parser = subparsers.add_parser(
        'systems', description=doc_split(systems))
    make_font_parser.set_defaults(func=systems)

    make_font_parser = subparsers.add_parser(
        'make', parents=[make_parser], description=doc_split(Font.make_font))
    make_font_parser.set_defaults(func=make_font)

    make_default_font_parser = subparsers.add_parser(
        'default', parents=[make_parser],
        description=doc_split(Font.make_default_font))
    make_default_font_parser.set_defaults(func=make_default_font)

    test_font_parser = subparsers.add_parser(
        'test', description=doc_split(print_charsets))
    test_font_parser.set_defaults(func=print_charsets)

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
