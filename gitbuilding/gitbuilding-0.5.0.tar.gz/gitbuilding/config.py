"""
This module deals with loading and parsing the configuration file
the main schema GBConfigSchema is subclassed from buildup.ConfigSchema.
All of extra GitBuilding specific options are added. The helper functions
for loading also deal with removing invalid configuration options and
logging a warning.
"""

import logging
from dataclasses import make_dataclass
import yaml
from marshmallow import Schema, fields, post_load
from gitbuilding.buildup import ConfigSchema

_LOGGER = logging.getLogger('BuildUp.GitBuilding')

def default_excludes():
    """
    Defines the default list of excluded files.
    """
    return ['README.md']

class HTMLOptSchema(Schema):
    """
    Marshmallow schema for parsing the HTML options. This includes custom headers and
    footers. Once loaded the schema creates a dataclass.
    """
    acknowledge_gitbuilding = fields.Bool(missing=True,
                                          data_key='AcknowledgeGitBuilding')
    custom_footer = fields.Str(missing=None, allow_none=True, data_key='CustomFooter')
    custom_header = fields.Str(missing=None, allow_none=True, data_key='CustomHeader')

    @post_load
    def make_object(self, data, **_): #pylint: disable=no-self-use
        """
        Auto generates a dataclass for the html options.
        """
        html_options = make_dataclass('HTMLOptions',
                                      data.keys())
        return html_options(**data)


class GBConfigSchema(ConfigSchema):
    """
    This is a subclass of buildup.ConfigSchema it is used to add all the extra
    configuration options to the base set of options used by BuildUp.
    """
    authors = fields.List(cls_or_instance=fields.Str, missing=list, data_key='Authors')
    affiliation = fields.Str(missing=None, allow_none=True, data_key='Affiliation')
    email = fields.Email(missing=None, allow_none=True, data_key='Email')
    fussy = fields.Bool(missing="True", data_key='Fussy')
    exclude = fields.List(cls_or_instance=fields.Str,
                          missing=default_excludes,
                          data_key='Exclude')
    website_root = fields.Url(missing="/",
                              relative=True,
                              require_tld=False,
                              data_key='WebsiteRoot')
    variables = fields.Dict(missing=dict,
                            keys=fields.Str(),
                            values=fields.Str(),
                            data_key='Variables')
    license = fields.Str(missing=None, allow_none=True, data_key='License')
    license_file = fields.Str(missing=None, allow_none=True, data_key='LicenseFile')
    html_options = fields.Nested(HTMLOptSchema,
                                 missing=HTMLOptSchema().load({}),
                                 data_key='HTMLOptions')

def load_config(config_dictionary):
    """
    Loads the build up configuration, any fields in the config_dictionary
    which fail validation are removed. Logging warnings are raised for
    each validation error. A dataclass object containing the
    validated configuration.
    """
    schema = GBConfigSchema()
    #Must run the validation twice as some keys validate off another
    for _ in range(2):
        warnings = schema.validate(config_dictionary)
        _log_warnings(warnings)
        for key in warnings:
            del config_dictionary[key]
        if warnings == {}:
            #break if there are no warnings
            break
    return schema.load(config_dictionary)

def load_config_from_file(yamlfile):
    """
    Runs load_config on the input yamlfile.
    """
    if yamlfile is None:
        return load_config({})
    with open(yamlfile, "r", encoding='utf-8') as stream:
        config_dictionary = yaml.load(stream, Loader=yaml.SafeLoader)
    return load_config(config_dictionary)

def _log_warnings(warnings, breadcrumbs=None):
    """
    The validator returns a nested dictionary of issues. Note that the top level
    option is removed in load_config if the validation fails
    """
    if breadcrumbs is None:
        breadcrumbs = []
    for key in warnings:
        if isinstance(warnings[key], dict):
            new_breadcrumbs = breadcrumbs[:]
            new_breadcrumbs.append(key)
            _log_warnings(warnings[key], new_breadcrumbs)
        else:
            if len(breadcrumbs) == 0:
                keys = key
                remkey = key
            else:
                remkey = breadcrumbs[0]
                keys = ''
                for crumb in breadcrumbs:
                    keys += str(crumb)+'->'
                keys += key
            _LOGGER.warning('Problem parsing configuration - %s: %s  '
                            'All configuration in %s will not be used.',
                            keys,
                            warnings[key][0],
                            remkey)
