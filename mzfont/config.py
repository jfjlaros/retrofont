from importlib import resources
from yaml import safe_load


def read_config():
    """
    """
    config_file = resources.files() / 'config.yaml'
    with config_file.open("rt") as config:
        return safe_load(config.read())


def select_system(systems, name):
    """
    """
    system = {
        'name': 'default',
        'mirror': False,
        'map_offset': 0,
        'default': [{'source': 'raw', 'range': [0x00, 0x100]}]}
    for configured_system in systems:
        if configured_system['name'] == name:
            system.update(configured_system)
            return system
    return system
