from os import environ

from retrofont.config import read_config, select_system_config


environ['HOME'] = ''  # Make sure the system config is used.
config = read_config()


def test_read_config():
    assert isinstance(config, dict)
    assert isinstance(config['font']['base'], str)
    assert isinstance(config['systems'], list)
    assert isinstance(config['systems'][0]['name'], str)


def test_select_system_config():
    systems = config['systems']
    name = systems[0]['name']
    system = select_system_config(systems, name)

    assert isinstance(system, dict)
    assert system['name'] == name
