#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Parent class for all connector and processor plugins
    provides methods for managing variables and stage references and their instantiation
"""

import re
from os import listdir
from os.path import isfile, join

from .utils.GeoEDFError import GeoEDFError

class GeoEDFPlugin:

    def __init__(self):

        # for each attribute, maintains a list of other attributes that it depends on
        # for each attribute, also maintain a list of other attributes that depend on it
        self.dependencies = dict()
        self.rev_dependencies = dict()
        self.stage_refs = dict()
        self.rev_stage_refs = dict()
        self.orig_vals = dict()

        # loop through the attributes of the object, parsing their value to
        # extract dependencies on other variables or prior stages
        for key in self.provided_params:
            self.orig_vals[key] = getattr(self,key)
            self.add_dependencies(key,getattr(self,key))

    # sets the plugin's type
    def set_plugin_type(self,plugin_type):
        self.plugin_type = plugin_type

    # resets parameters that have variables in value to their original values
    # this needs to be run first, each time a new variable binding is instantiated
    # may not need this method if we will be running a new job for each binding
    def reset_bindings(self):
        for key in self.dependencies:
            setattr(self,key,self.orig_vals[key])

    # find all variables mentioned in value
    def find_vars(self,value):
        if value is not None and isinstance(value,str):
            return re.findall('\%\{(.+)\}',value)
        else:
            return []

    # find all prior stages referenced in value
    def find_stage_refs(self,value):
        if value is not None and isinstance(value,str):
            return re.findall('\$([0-9]+)',value)
        else:
            return []

    # find all variables mentioned by this plugin
    def find_vars_used(self):
        return list(self.rev_dependencies.keys())

    # find all stages referenced by this plugin
    def find_stages_referenced(self):
        return list(self.rev_stage_refs.keys())

    # parse the value, adding any variable names or stage references to key's dependencies
    def add_dependencies(self,key,value):

        # find parameters mentioned in the value
        key_dependencies = self.find_vars(value)

        if len(key_dependencies) > 0:

            # set dependencies
            self.dependencies[key] = key_dependencies

            # set reverse dependencies
            for dep_key in key_dependencies:
                if dep_key in self.rev_dependencies:
                    self.rev_dependencies[dep_key].append(key)
                else:
                    self.rev_dependencies[dep_key] = [key]

        # find stages referenced in value
        stage_refs = self.find_stage_refs(value)

        if len(stage_refs) > 0:
            if len(stage_refs) > 1:
                raise GeoEDFError("At most one prior stage's output can be referenced in a binding")
            
            # the only stage ref in this value
            stage_ref = stage_refs[0]
            self.stage_refs[key] = stage_refs

            if stage_ref in self.rev_stage_refs:
                self.rev_stage_refs[stage_ref].append(key)
            else:
                self.rev_stage_refs[stage_ref] = [key]

    # instantiate a set of variable bindings, updating values of any dependent attributes
    def bind_vars(self,var_bind_dict):
        # loop over the variables, only considering dependencies for this plugin
        for var in var_bind_dict.keys():
            if var in self.rev_dependencies:
                value = var_bind_dict[var]
                # loop over every attribute that depends on this variable
                for attr_key in self.rev_dependencies[var]:
                    # (partially) instantiate the dependent attribute
                    dep_val = getattr(self,attr_key)
                    needle = '%{{{}}}'.format(var)
                    setattr(self,attr_key,dep_val.replace(needle,value))

    # instantiate any stage references; apply any "dir" modifiers before setting value on param
    def bind_stage_refs(self,stage_ref_dict):
        # loop over the stages with bindings, only considering stages referenced in this plugin
        for stage in stage_ref_dict.keys():
            if stage in self.rev_stage_refs:
                stage_ref_val = stage_ref_dict[stage]
                # loop over attributes that reference this stage
                for attr_key in self.rev_stage_refs[stage]:

                    # instantiate the attribute's value with the stage reference
                    dep_val = getattr(self,attr_key)
                    # first determine number of dir modifiers
                    num_dir_modifiers = self.count_dir_modifiers(dep_val)

                    # if no dir modifiers, then simply instantiate with stage reference value
                    if num_dir_modifiers == 0:
                        setattr(self,attr_key,stage_ref_val)
                    else: # apply dirname repeatedly
                        temp_val = stage_ref_val
                        while num_dir_modifiers > 0:
                            temp_val = dirname(temp_val)
                            num_dir_modifiers -= 1
                        setattr(self,attr_key,temp_val)

    # set values for args left blank (sensitive args)
    def bind_sensitive_args(self,sensitive_arg_bindings_dict):
        for arg in sensitive_arg_bindings_dict.keys():
            val = sensitive_arg_bindings_dict[arg]
            setattr(self,arg,val)
                            
    # updates arg values with these overrides
    def set_arg_overrides(self,arg_overrides_dict):
        # loop through args needing overriding
        for arg in arg_overrides_dict.keys():
            override_val = arg_overrides_dict[arg]
            setattr(self,arg,override_val)

    # sets the target path for this plugin's outputs
    def set_output_path(self,path):
        self.target_path = path
                        
    # saves the outputs of a filter plugin to a text file to return to the
    # workflow engine
    # assume only invoked on filter plugins
    def save_filter_outputs(self):
        with open(self.target_path,'w') as output_file:
            for val in self.values:
                output_file.write('%s\n' % val)

    # determine the number of "dir" modifiers in a value containing a stage reference 
    # assumes validation has already occurred on the value string
    def count_dir_modifiers(self,value):
        count = 0
        while(value.startswith('dir(')):
            count += 1
            value = value[4:]
        return count
        
