# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.assess.policy.propagation_node import PropagationNode
from contrast.agent.assess.policy.source_node import SourceNode
from contrast.agent.assess.policy.trigger_node import TriggerNode


class PatchLocationPolicy(object):
    """
    Container for all policy nodes that pertain to a single patch location

    A patch location is a specific function or method that we patch. A single patch
    location may correspond to multiple policy nodes. Since import hooks are applied at
    the module level, there is a one-to-many relationship between each module and the
    corresponding PatchLocationPolicy instances.
    """

    def __init__(self, node):
        self.module = node.module
        self.class_name = node.class_name
        self.method_name = node.method_name
        # This is a copy of the name attribute of each PolicyNode represented by this
        # PatchLocationPolicy instances. All policy nodes represented by this location
        # must have the same name.
        self.name = node.name

        self.source_nodes = []
        self.propagator_nodes = []
        self.trigger_nodes = []
        self.patch_locations = []

    def add_node(self, node):
        """
        Add a policy node for this patch location
        """
        # This is a sanity check to ensure that we don't accidentally add a node that
        # corresponds to a different patch location.
        assert node.name == self.name

        if isinstance(node, PropagationNode):
            self.propagator_nodes.append(node)
        elif isinstance(node, SourceNode):
            self.source_nodes.append(node)
        elif isinstance(node, TriggerNode):
            self.trigger_nodes.append(node)

    @property
    def has_patches(self):
        """
        Indicates whether any nodes at this location require policy patches
        """
        return any([node.policy_patch for node in self.all_nodes()])

    def all_nodes(self):
        """
        Returns all nodes in this policy as a list
        """
        return self.source_nodes + self.propagator_nodes + self.trigger_nodes

    def __repr__(self):
        return "<{0.__class__.__name__}({0.name})>".format(self)
