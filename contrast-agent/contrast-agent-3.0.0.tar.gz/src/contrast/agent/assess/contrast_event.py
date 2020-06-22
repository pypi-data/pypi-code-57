# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import threading
from inspect import getframeinfo

from contrast.extern import six

from contrast.agent.assess.policy_constants import ALL_KWARGS, OBJECT, RETURN
from contrast.agent.assess.utils import get_properties
from contrast.api.dtm_pb2 import (
    ParentObjectId,
    TraceEvent,
    TraceEventObject,
    TraceEventSource,
    TraceStack,
)
from contrast.utils.assess.tracking_util import is_tracked
from contrast.utils.base64_utils import base64_encode
from contrast.utils.object_utils import safe_copy
from contrast.utils.stack_trace_utils import StackTraceUtils
from contrast.utils.string_utils import protobuf_safe
from contrast.utils.timer import Timer


class ContrastEvent(object):
    """
    This class holds the data about an event in the application
    We'll use it to build an event that TeamServer can consume if
    the object to which this event belongs ends in a trigger.
    """

    ATOMIC_ID = 0
    ELLIPSIS = "..."
    UNTRUNCATED_PORTION_LENGTH = 25
    TRUNCATION_LENGTH = (UNTRUNCATED_PORTION_LENGTH * 2) + 3  # ELLIPSIS length
    INITIALIZERS = ("__init__", "__new__")
    NONE_STRING = str(None)

    TRACE_EVENT_TYPE_MAP = {"METHOD": 0, "PROPAGATOR": 1, "TAGGER": 2, "TAG": 2}

    def __init__(
        self,
        node,
        tagged,
        self_obj,
        ret,
        args,
        kwargs,
        parent_ids,
        possible_key,
        source_type=None,
        source_name=None,
        frame=None,
    ):
        self._stack_trace = self.populate_stack_trace()

        self.caller = self._stack_trace[0] if self._stack_trace else None

        self.node = node
        self.time = Timer.now_ms()

        self.thread = threading.current_thread().ident

        self.source_type = source_type
        self.source_name = source_name

        self.event_id = ContrastEvent._atomic_id()
        self.parent_ids = parent_ids

        self.obj = None
        self.ret = None
        self.args = None
        self.kwargs = {}

        self.possible_key = possible_key

        self.highlight = None

        self.populate_method_information(self_obj, ret, args, kwargs, tagged)

        self.frameinfo = getframeinfo(frame) if frame is not None else frame

    def populate_stack_trace(self):
        try:
            return StackTraceUtils.build(ignore=True, depth=20, for_trace=True)
        except Exception:
            return []

    @classmethod
    def _atomic_id(cls):
        ret = cls.ATOMIC_ID

        cls.ATOMIC_ID += 1

        return ret

    def populate_method_information(self, self_obj, ret, args, kwargs, tagged):
        target = self.get_target_from_node()

        self.args = safe_copy(args)
        self.kwargs = safe_copy(kwargs)

        if target is None:
            # If the target is None, this rule was violated simply by a method
            # being called. We'll save all the information, but nothing will be
            # marked up, as nothing need be tracked
            self.obj = self_obj
            self.ret = ret
            return

        if target == OBJECT:
            self.obj = tagged
            self.ret = ret
            return

        if target == RETURN:
            self.obj = self_obj
            self.ret = tagged
            return

        # If the target is ALL_ARGS, then we need to dup things
        # a little differently. We need to find the true
        # target inside so that we can mark it up later.
        self.obj = self_obj
        self.ret = ret

        if isinstance(target, int) and tagged not in self.args:
            # TODO: This is really questionable logic and it should be removed.
            # The problem is that we are not passing the args properly in some
            # of our triggers, and so this has been added as a workaround so
            # that the args are reported appropriately. For example, look at
            # contrast.applies.common.applies_sqli_rule. In this case, we break
            # the first argument out as sql, but we never pass that particular
            # argument into the args used to build the event -_-. See PYT-388.
            temp_list = list(self.args)
            temp_list.insert(target, tagged)
            self.args = tuple(temp_list)
            return

        # iterate over kwargs and not self.kwargs because we are modifying the latter.
        for keyword in kwargs:
            if target == keyword:
                # TODO: determine if we should be modifying self.kwargs instead
                kwargs[keyword] = tagged
                self.highlight = keyword
                break

    def get_target_from_node(self):
        if self.node.targets:
            return self.node.targets[0]

        if self.node.sources:
            return self.node.sources[0]

    def add_taint_ranges(self, event, taint_target, target, splat):
        properties = None

        if splat is not None:
            properties = get_properties(target)
            if properties is None:
                return

            tag_ranges = properties.tags_to_dtm(splat_range=(0, splat))
            event.taint_ranges.extend(tag_ranges)
            return

        if taint_target is None:
            return

        if isinstance(target, dict):
            if taint_target == ALL_KWARGS and self.possible_key:
                properties = get_properties(target.get(self.possible_key, None))
            else:
                properties = get_properties(target.get(taint_target, None))
        else:
            properties = get_properties(target)

        if properties is None:
            return

        event.taint_ranges.extend(properties.tags_to_dtm())

    def build_event_args(self, event, taint_target):
        for index, arg in enumerate(self.args):
            is_taint_target = taint_target == index

            trace_object = TraceEventObject()
            splat = self.build_event_object(trace_object, arg, not is_taint_target)
            event.args.extend([trace_object])
            if is_taint_target:
                self.add_taint_ranges(event, taint_target, arg, splat)

    def build_event_objects(self, event):
        taint_target = self.determine_event_source_target_and_taint(event)

        objects = [
            (event.object, self.obj, OBJECT),
            (event.ret, self.ret, RETURN),
        ]

        for event_obj, obj, key in objects:
            is_taint_target = taint_target == key
            splat = self.build_event_object(event_obj, obj, not is_taint_target)
            if is_taint_target:
                self.add_taint_ranges(event, taint_target, obj, splat)

        self.build_event_args(event, taint_target)

        if self.kwargs:
            # TODO: handle tainted kwargs
            trace_object = TraceEventObject()
            splat = self.build_event_object(trace_object, str(self.kwargs), True)
            event.args.extend([trace_object])
            if taint_target is ALL_KWARGS or isinstance(taint_target, str):
                self.add_taint_ranges(event, taint_target, self.kwargs, splat)

    def to_dtm_event(self):
        event = TraceEvent()

        event.type = self.TRACE_EVENT_TYPE_MAP.get(self.node.node_type, 1)
        event.action = self.node.build_action()
        event.timestamp_ms = self.time
        event.thread = str(self.thread)

        self.build_event_objects(event)

        if self.frameinfo:
            self.convert_frameinfo(self.frameinfo, event)

        for frame in self._stack_trace:
            self.convert_stack_frame_element(frame, event)

        safe_source_name = protobuf_safe(self.source_name)
        event.field_name = safe_source_name

        if self.source_type:
            event.event_sources.extend([self.build_source_event(safe_source_name)])

        event.object_id = int(self.event_id)

        if self.parent_ids:
            for parent_id in self.parent_ids:
                parent = ParentObjectId()
                parent.id = parent_id
                event.parent_object_ids.extend([parent])

        self.build_complete_signature(event)

        return event

    def build_event_object(self, event_object, self_obj, truncate):
        obj_string, splat = self.obj_to_str(self_obj)

        if truncate and len(obj_string) > self.TRUNCATION_LENGTH:
            temp = [
                obj_string[0 : self.TRUNCATION_LENGTH],
                self.ELLIPSIS,
                obj_string[
                    len(obj_string)
                    - self.UNTRUNCATED_PORTION_LENGTH : self.UNTRUNCATED_PORTION_LENGTH
                ],
            ]

            obj_string = "".join(temp)

        event_object.value = base64_encode(obj_string)
        event_object.tracked = is_tracked(self_obj)

        return len(obj_string) if splat else None

    def obj_to_str(self, self_obj):
        """
        Attempt to get a string representation of an object

        Right now we do our best to decode the object, but we handle any
        decoding errors by replacing with �. This technically is a loss
        of information when presented in TS, but it allows us to preserve
        the taint range information, which arguably is more important for
        Assess. In the future we might want to implement more robust
        handling of non-decodable binary data (i.e. to display escaped
        data with an updated taint range).

        If the object isn't stringy, then just return the string
        representation. In this case, we will need to splat the displayed
        taint range since we're not able to map tag ranges.

        :param self_obj: any python object, str, byte, bytearray, etc
        :return:
            1. str representing the object
            2. whether to splat the taint ranges or not, depending on if we can stringify the obj
        """
        splat = False

        try:
            if isinstance(self_obj, bytearray):
                obj_string = self_obj.decode(errors="replace")
            else:
                obj_string = six.ensure_str(self_obj, errors="replace")
        except TypeError:
            obj_string = str(self_obj)
            splat = True

        return obj_string, splat

    def build_source_event(self, safe_source_name):
        """
        Create a new TraceEventSource

        :param safe_source_name: source name or empty string
        :return: TraceEvenSource
        """
        trace_event_source = TraceEventSource()

        trace_event_source.type = self.source_type
        trace_event_source.name = safe_source_name

        return trace_event_source

    def build_complete_signature(self, event):
        return_type = type(self.ret).__name__ if self.ret else self.NONE_STRING

        event.signature.return_type = return_type
        # We don't want to report "BUILTIN" as a module name in Team Server
        event.signature.class_name = self.node.location.replace("BUILTIN.", "")
        event.signature.method_name = self.node.method_name

        if self.args:
            for item in self.args:
                arg_type = type(item).__name__ if item else self.NONE_STRING
                event.signature.arg_types.append(arg_type)

        if self.kwargs:
            arg_type = type(self.kwargs).__name__
            event.signature.arg_types.append(arg_type)

        event.signature.constructor = self.node.method_name in self.INITIALIZERS

        # python always returns None if not returned
        event.signature.void_method = False

        if not self.node.instance_method:
            event.signature.flags = 8

    def determine_event_source_target_and_taint(self, event):
        """
        We have to do a little work to figure out what our TS appropriate
        target is. To break this down, the logic is as follows:
        1) If my node has a target, work on targets. Else, work on sources.
           Per TS law, each node must have at least a source or a target.
           The only type of node w/o targets is a Trigger, but that may
           change.
        2) If I have a highlight, it means that I have a P target that is
           not in integer form (it was a named / keyword type for which I had
           to find the index). I need to address this so that TS can process
           it.
        3) I'll set the event's source and target to TS values.
        4) Return the highlight or the first source/target as the taint
           target.
        """
        if self.node.targets:
            if self.node.source_string:
                event.source = self.node.source_string

            event.target = (
                "P{}".format(self.highlight)
                if self.highlight
                else self.node.target_string
            )

            if self.highlight:
                return self.highlight
            return self.node.targets[0]

        if self.node.sources:
            event.source = (
                "P{}".format(self.highlight)
                if self.highlight
                else self.node.source_string
            )

            if self.node.target_string:
                event.source = self.node.target_string

            if self.highlight:
                return self.highlight

            return self.node.sources[0]

    def convert_frameinfo(self, frame, event):
        """
        Used to convert actual python frame object
        """
        stack = TraceStack()
        stack.line_number = frame.lineno

        stack.method_name = protobuf_safe(self.node.method_name)
        stack.declaring_class = protobuf_safe(frame.filename)
        stack.file_name = protobuf_safe(frame.filename)
        event.stack.extend([stack])

    def convert_stack_frame_element(self, frame, event):
        """
        Used to convert a dtm StackFrameElement to a TraceStack

        protobuf_safe(frame.declaring_class)
        """
        frame.declaring_class = frame.file_name

        file_name = protobuf_safe(frame.file_name)

        frame.file_name = file_name

        event.stack.extend([frame])
