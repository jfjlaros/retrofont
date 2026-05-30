from importlib import resources
from os.path import exists, expanduser
from yaml import safe_load


def _get_config_file() -> str:
    config_sys = str(resources.files(__package__) / 'config.yaml')
    config_user = expanduser('~/.config/retrofont/config.yaml')
    return config_user if exists(config_user) else config_sys


def read_config() -> dict:
    """Read the content of the configuration file.

    :return: Configuration.
    """
    config_file = _get_config_file()
    with open(config_file, "rt") as config:
        return safe_load(config.read())


def select_system_config(systems: dict, name: str) -> dict:
    """Select a configured system.

    :arg name: System name.

    :return: System configuraion.
    """
    for configured_system in systems:
        if configured_system['name'] == name:
            return configured_system
    return {}
