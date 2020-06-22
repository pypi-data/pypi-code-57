# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern.six import PY2, PY3, integer_types

from contrast.agent.assess import policy_constants
from contrast.agent.assess.assess_exceptions import ContrastAssessException
from contrast.agent.assess.policy_constants import ALL_ARGS, OBJECT, RETURN
from contrast.api.dtm_pb2 import TraceEvent
from contrast.utils.object_share import ObjectShare


class PolicyNode(object):
    def __init__(
        self,
        module="",
        class_name="",
        instance_method=True,
        method_name="",
        source="",
        target="",
        tags=None,
        policy_patch=True,
        python2_only=False,
        python3_only=False,
    ):
        self.module = module
        self.class_name = class_name

        # If no class_name is given, it indicates that this node corresponds to a
        # standalone function, not a method. This means that instance_method is always
        # False. Otherwise we use the given value of instance_method. However, the
        # default for this argument will be True if not given for all policy nodes,
        # which means that only methods that are **not** instance methods must provide
        # it explicitly. This value is used to determine whether or not the first
        # positional argument should be treated as "self" or not by our policy
        # machinery
        self.instance_method = instance_method if class_name else False

        self.method_name = method_name

        self.sources = self.parse_source_or_target(source)
        self.targets = self.parse_source_or_target(target)

        self.source_string = self.ts_represent(source)
        self.target_string = self.ts_represent(target)

        self.tags = set()

        if tags:
            self.tags.update(tags)

        # This attribute indicates whether a given policy node corresponds to a patch
        # that should be applied by policy. It defaults to True. However, many of our
        # policy nodes are **not** patched by policy but instead are patched in a
        # different way. For example, nearly all of our string propagators are applied
        # as C hooks. In these cases we still use the policy node for reporting
        # purposes, but we don't want a policy patch.
        self.policy_patch = policy_patch

        self.python2_only = python2_only
        self.python3_only = python3_only

        self.properties = {}

        self.event_action = None

    @property
    def name(self):
        """
        Fully specified unique name for this node

        Includes module name, class name (if applicable) and method name
        """
        return "{}.{}".format(self.location, self.method_name)

    @property
    def location(self):
        """
        Property indicating the fully specified location of the patched method/function

        For a method of a class:
            <module_path>.<class_name>.<method_name>

        For a function:
            <module_path>.<function_name>
        """
        return "{}{}".format(
            self.module, "." + self.class_name if self.class_name else ""
        )

    def add_property(self, name, value):
        if not name or not value:
            return

        self.properties[name] = value

    def get_property(self, name):

        if not self.properties:
            return

        return self.properties[name]

    @property
    def node_class(self):
        return self.__class__.__name__.replace("Node", "")

    @property
    def node_type(self):
        return "TYPE_METHOD"

    @property
    def version_mismatch(self):
        """
        Indicates whether this node is incompatible with the current Python version

        Currently the finest granularity we have is Py2.7 vs Py3, but eventually we may
        update it to have more specific version specifications.
        """
        return (PY2 and self.python3_only) or (PY3 and self.python2_only)

    def parse_source_or_target(self, str_rep):
        """
        Given a string source or target, split it into its list representation
        by splitting on ',' and appending the appropriate represntation to the list.

        :param str_rep: string representation of a source or target, such as 'ARG_0, OBJ'
        :return: list representation of source or target, [0, 'OBJ']
        """
        ret = []

        if not str_rep:
            return []

        for item in str_rep.split(ObjectShare.COMMA):
            if item == policy_constants.OBJECT:
                ret.append(item)

            elif item == policy_constants.RETURN:
                ret.append(item)

            elif item == policy_constants.ALL_ARGS:
                ret.append(policy_constants.ALL_ARGS)

            elif item == policy_constants.ALL_KWARGS:
                ret.append(policy_constants.ALL_KWARGS)

            # handle ARG_#
            elif item.startswith(policy_constants.ARG + ObjectShare.UNDERSCORE):
                arg_num = item.split(ObjectShare.UNDERSCORE)[1]
                ret.append(int(arg_num))

            # handle KWARG:name
            elif item.startswith(policy_constants.KWARG + ObjectShare.COLON):
                kwarg_name = item.split(ObjectShare.COLON)[1]
                ret.append(kwarg_name)

            else:
                return []

        return ret

    def ts_represent(self, str_rep):
        if not str_rep:
            return None
        return str_rep.replace("ARG_", "P")

    def get_matching_first_target(self, self_obj, ret, args, kwargs):
        node_target = self.targets[0]

        if node_target is None:
            return

        if node_target == ALL_ARGS:
            return args

        if node_target == RETURN:
            return ret

        if node_target == OBJECT:
            return self_obj

        if args and isinstance(node_target, integer_types):
            return args[node_target]

        if kwargs and node_target in kwargs:
            return kwargs[node_target]

    def validate(self):
        if not self.module:
            raise ContrastAssessException(
                "{} unknown did not have a proper module. Unable to create.".format(
                    self.node_class
                )
            )

        if not self.method_name:
            raise ContrastAssessException(
                "{} did not have a proper method name. Unable to create.".format(
                    self.node_class
                )
            )

        self.validate_tags()

    def validate_tags(self):
        if not self.tags:
            return

        for item in self.tags:
            if not (
                item in policy_constants.VALID_TAGS
                or item in policy_constants.VALID_SOURCE_TAGS
            ):
                raise ContrastAssessException(
                    "{} {} had an invalid tag. {} is not a known value.".format(
                        self.node_class, self.name, item
                    )
                )

    def _type_to_action(self, src_or_target):
        """
        Convert a source or target string into a TS-valid action string.
        """
        if ObjectShare.COMMA in src_or_target:
            return policy_constants.ALL_TYPE

        if src_or_target == policy_constants.OBJECT:
            return policy_constants.OBJECT_KEY

        if src_or_target in (policy_constants.ALL_ARGS, policy_constants.ALL_KWARGS):
            return policy_constants.ALL_TYPE

        if src_or_target.startswith(
            policy_constants.ARG_OR_KWARG
        ) or src_or_target.startswith(policy_constants.KWARG + ObjectShare.COLON):
            return policy_constants.ARG_OR_KWARG

        # only target, not source, can be return type
        if src_or_target == policy_constants.RETURN:
            return policy_constants.RETURN_KEY

    def build_action(self):
        """
        Convert our action, built from our source and target, into
        the TS appropriate action.

        Creation (source nodes) don't have sources (they are the source)
        Trigger (trigger nodes) don't have targets (they are the target)
        Everything else (propagation nodes) are Source2Target
        :return: self.event_action
        """
        if self.event_action is None:
            source = self.source_string
            target = self.target_string

            if source is None:
                self.event_action = TraceEvent.Action.Value(
                    policy_constants.CREATION_TYPE
                )
            elif target is None:
                self.event_action = TraceEvent.Action.Value(
                    policy_constants.TRIGGER_TYPE
                )
            else:
                source = self._type_to_action(source)
                target = self._type_to_action(target)
                str_action = source + policy_constants.TO_MARKER + target

                self.event_action = TraceEvent.Action.Value(str_action)

        return self.event_action

    def __repr__(self):
        return "{} - {}".format(self.__class__.__name__, self.name)
