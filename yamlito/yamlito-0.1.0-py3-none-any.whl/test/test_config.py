import io
import pytest

import yamlito.config as config

simple_custom = 'Charm: \n' \
                '  label: Charmino\n'


@pytest.fixture
def default_yaml():
    return io.StringIO("Charm: \n"
                       "  label: Charm Quark\n"
                       "  mass: 1.275\n"
                       "  brothers: \n"
                       "    favorite: [strange, bottom]\n"
                       "    evil_twin: anti-charm\n")


@pytest.fixture()
def default_parsed_dict():
    return {'Charm':
                {'label': 'Charm Quark',
                 'mass': 1.275,
                 'brothers':
                     {'favorite': ['strange', 'bottom'],
                      'evil_twin': 'anti-charm'}}}


@pytest.fixture
def custom_user_dict():
    return {'Charm':
                {'brothers':
                     {'favorite': ['up', 'down']}}}


@pytest.fixture
def custom_user_yaml():
    return io.StringIO("Charm: \n"
                       "  brothers: \n"
                       "    favorite: ['up', 'down']\n")


@pytest.fixture
def custom_user_parsed_dict():
    return {'Charm':
                {'label': 'Charm Quark',
                 'mass': 1.275,
                 'brothers':
                     {'favorite': ['up', 'down'],
                      'evil_twin': 'anti-charm'}}}


def test__update_dict_first_level(default_parsed_dict):
    config._update_dict(default_parsed_dict,
                        {'Charm': {'label': 'Charmino'}})

    correct = {'Charm':
                   {'label': 'Charmino',
                    'mass': 1.275,
                    'brothers':
                        {'favorite': ['strange', 'bottom'],
                         'evil_twin': 'anti-charm'}}}

    assert default_parsed_dict == correct


def test__update_dict_second_level_item(default_parsed_dict):
    config._update_dict(default_parsed_dict,
                        {'Charm':
                             {'brothers':
                                  {'evil_twin': 'c-bar'}}})

    correct = {'Charm':
                   {'label': 'Charm Quark',
                    'mass': 1.275,
                    'brothers':
                        {'favorite': ['strange', 'bottom'],
                         'evil_twin': 'c-bar'}}}

    assert default_parsed_dict == correct


def test__update_dict_second_level_list(default_parsed_dict, custom_user_dict,
                                        custom_user_parsed_dict):
    config._update_dict(default_parsed_dict,
                        custom_user_dict)

    assert default_parsed_dict == custom_user_parsed_dict


def test__read_config_simple_file(default_yaml, default_parsed_dict):
    assert config._read_config_file(default_yaml) == default_parsed_dict


def test__read_config_file_invalid_yaml():
    invalid_yaml_file = io.StringIO("aa:\naaa")
    with pytest.raises(ValueError):
        config._read_config_file(invalid_yaml_file)


def test_read_config_only_default_file(default_yaml, default_parsed_dict):
    assert config.read_config(default_yaml) == default_parsed_dict


def test_read_config_custom_user_file(default_yaml, custom_user_yaml, custom_user_parsed_dict):
    assert config.read_config(default_yaml, custom_user_yaml) == custom_user_parsed_dict


def test_config_default_constructor(default_parsed_dict):
    config_charm = config.Config(**default_parsed_dict["Charm"])
    assert config_charm.label == 'Charm Quark'
    assert config_charm.mass == 1.275
    assert config_charm.brothers.favorite == ['strange', 'bottom']
    assert config_charm.brothers.evil_twin == 'anti-charm'


def test_config_default_parse(default_parsed_dict):
    config_charm = config.Config.parse(default_parsed_dict["Charm"])
    assert config_charm.label == 'Charm Quark'
    assert config_charm.mass == 1.275
    assert config_charm.brothers.favorite == ['strange', 'bottom']
    assert config_charm.brothers.evil_twin == 'anti-charm'


def test_config_default_representation(default_parsed_dict):
    assert repr(config.Config.parse(
        default_parsed_dict)) == " <Charm: <label:'Charm Quark'> <mass:1.275> <brothers: " \
                                 "<favorite:['strange', 'bottom']> <evil_twin:'anti-charm'>>>"


def test_config_to_dict():
    complicated_dict_config = {
        'Charm':
            {'label': 'Charm Quark',
             'mass': 1.275,
             'brothers':
                 {'favorite': ['strange', 'bottom'],
                  'evil_twin': 'anti-charm'}},
        'mystic':
            {'type':
                 {'super_nested':
                      {'hidden': 'nothing',
                       'deeper':
                           {'secret':
                                {'funny': 'over',
                                 'not_so_funny': 13}}},
                  'not_so_nested': ''}}}
    assert config.Config.parse(complicated_dict_config).to_dict() == complicated_dict_config
