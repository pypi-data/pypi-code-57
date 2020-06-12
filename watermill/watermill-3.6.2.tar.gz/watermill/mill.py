from dataclasses import asdict
from dataclasses import is_dataclass
from logging import getLogger
from typing import Callable
from typing import Dict
from typing import Generator
from typing import List
from typing import Mapping
from typing import NoReturn
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union
from typing import get_type_hints

from botox import Injector

from watermill.message_brokers.message_broker import EndOfStream
from watermill.message_brokers.message_broker import EndOfStreamError
from watermill.message_brokers.message_broker import MessageBroker
from watermill.message_brokers.message_broker import RightJoinedStreamRanAhead
from watermill.message_brokers.message_broker import StreamTimeoutError
from watermill.message_brokers.message_broker import StreamsShift
from watermill.stream_join import JoinTree
from watermill.stream_join import JoinTreeNode
from watermill.stream_join import compare_streams
from watermill.stream_join import get_injected_kwargs
from watermill.stream_join import get_join_data_mapping
from watermill.stream_join import get_tree_pairs
from watermill.message_brokers.message_broker import DataKey
from watermill.stream_types import AliasType
from watermill.stream_types import JoinedStreamType
from watermill.stream_types import ResultStreamType
from watermill.stream_types import StreamType
from watermill.windows import Window
import dataclass_factory


logger = getLogger(__name__)


def _default_serializer(dataclass_value) -> dict:
    assert is_dataclass(dataclass_value)
    return asdict(dataclass_value)


factory = dataclass_factory.Factory()


def _default_deserializer(cls):
    if isinstance(cls, AliasType):
        cls = cls.origin_cls
    def wrapped_de(value: dict):
        return factory.load(value, cls)
    return wrapped_de


class WaterMill:
    def __init__(
            self,
            broker: MessageBroker,
            process_func: Callable[[StreamType, List[Mapping[StreamType, JoinedStreamType]]], Union[ResultStreamType, None]],
            stream_cls: Union[Type[StreamType], Window] = None,
            join_tree: JoinTree = None,
            serializers: Mapping[Type, Callable] = None,
            deserializers: Mapping[Type, Callable] = None,
            injector: Injector = None,
            output_broker: Optional[MessageBroker] = None,
            explicit_return_types: List[StreamType] = None
    ):
        assert stream_cls or join_tree

        self._injector = injector or Injector()
        self._injector.prepare(WaterMill, self)
        self._broker = broker
        self._output_broker = output_broker or broker
        self._window_func = None
        self._eos = False
        self._data_keys_to_send = set()
        self._explicit_return_types = explicit_return_types
        type_hints = get_type_hints(process_func)
        self._return_type = type_hints.get('return')
        if self._return_type == NoReturn or self._return_type == type(None):
            self._return_type = None
        elif str(self._return_type).startswith('typing.Union'):
            for return_type_item in self._return_type.__reduce__()[1][1]:
                if return_type_item != NoReturn:
                    self._return_type = return_type_item
                    break

        if stream_cls:
            if isinstance(stream_cls, Window):
                self._join_tree = JoinTree(
                    root_node=JoinTreeNode(
                        user_type=stream_cls.cls,
                    )
                )
                self._window_func = stream_cls.window_func
            else:
                self._join_tree = JoinTree(
                    root_node=JoinTreeNode(
                        user_type=stream_cls,
                    )
                )
        else:
            self._join_tree = join_tree

        self._process_func = process_func
        self._serializers: Mapping[Type, Callable] = serializers or {}
        self._deserializers: Mapping[Type, Callable] = deserializers or {}

    def run(self):
        if self._join_tree is None:
            return

        join_tree = self._join_tree
        serializer = self._serializers.get(self._return_type, _default_serializer) if self._return_type else None
        deserializer = self._deserializers.get(join_tree.root_node.user_type, _default_deserializer(join_tree.root_node.user_type))
        processing_func_type_hints = get_type_hints(self._process_func)
        current_key = None
        self._injector.prepare(DataKey, lambda: current_key)

        window_key = None
        root_elements = []
        join_data_mappings = []
        process_results = []
        window_func = self._window_func
        if join_tree.root_node.window_func:
            window_func = join_tree.root_node.window_func

        window_comparator = lambda next_element: StreamsShift.Equal if (window_key is None or window_key == window_func(next_element)) else StreamsShift.Less

        while True:
            root_element_data = None
            eos = False
            try:
                root_element_data = next(self._broker.get_elements(join_tree.root_node.user_type, comparator=window_comparator))
                current_key = self._broker.get_data_key()
            except RightJoinedStreamRanAhead:
                injected_kwargs = get_injected_kwargs(processing_func_type_hints, self._injector)
                if current_key:
                    self._data_keys_to_send.add(current_key.key)
                process_result = self._process_func(root_elements, *join_data_mappings, **injected_kwargs)
                process_results, eos = _handle_result(process_result, process_results, eos)
                root_elements.clear()
                join_data_mappings.clear()
                window_key = None
            except StreamTimeoutError:
                eos = True
                if window_func:
                    new_window_key = window_func(None)

                    assert new_window_key is not None
                    if window_key and window_key != new_window_key and root_elements:
                        injected_kwargs = get_injected_kwargs(processing_func_type_hints, self._injector)
                        if current_key:
                            self._data_keys_to_send.add(current_key.key)
                        process_result = self._process_func(root_elements, *join_data_mappings, **injected_kwargs)
                        process_results, eos = _handle_result(process_result, process_results, eos)
                        root_elements.clear()
                        join_data_mappings.clear()
                        window_key = new_window_key
            except EndOfStreamError:
                if self._return_type:
                    self._output_broker.send_eos(self._return_type)
                elif not self._data_keys_to_send and self._explicit_return_types:
                    for explicit_return_type in self._explicit_return_types:
                        self._output_broker.send_eos(explicit_return_type)
                self._eos = True
                return

            join_data_mapping = []
            if root_element_data:
                root_user_element = deserializer(root_element_data)
                if join_tree.pairs:
                    parent_children_map: Dict[StreamType, List[JoinedStreamType]] = {}
                    try:
                        self._get_joined_elements(join_tree.root_node, join_tree, root_element_data, root_user_element, parent_children_map)
                        if current_key:
                            current_key =  self._broker.get_data_key()
                    except RightJoinedStreamRanAhead as exc:
                        if not window_func:
                            logger.warning(f'Joined right stream {exc.stream_type} ran ahead. Skipping root element')
                            continue
                    except EndOfStreamError:
                        self._eos = True
                        if parent_children_map:
                            eos = True
                        elif self._return_type:
                            self._output_broker.send_eos(self._return_type)
                            self._broker.commit()
                            return
                        elif not self._data_keys_to_send and self._explicit_return_types:
                            for explicit_return_type in self._explicit_return_types:
                                self._output_broker.send_eos(explicit_return_type)
                            return

                    join_data_mapping = get_join_data_mapping(processing_func_type_hints, parent_children_map)

                if window_func:
                    new_window_key = window_func(root_element_data)
                    assert new_window_key is not None
                    root_elements.append(root_user_element)
                    if not join_data_mappings:
                        join_data_mappings = join_data_mapping
                    else:
                        assert len(join_data_mapping) == len(join_data_mappings)
                        temp_join_data_mappings = []
                        for old, new in zip(join_data_mappings, join_data_mapping):
                            old.update(new)
                            temp_join_data_mappings.append(old)
                        join_data_mappings = temp_join_data_mappings

                    if eos:
                        if root_user_element and not isinstance(root_user_element, EndOfStream):
                            try:
                                while True:
                                    next_root_element_data = next(
                                        self._broker.get_elements(
                                            join_tree.root_node.user_type,
                                            comparator=window_comparator
                                        )
                                    )

                                    next_window_key = window_func(next_root_element_data)
                                    if next_window_key == new_window_key:
                                        new_window_key = next_window_key
                                        next_root_element = deserializer(next_root_element_data)
                                        root_elements.append(next_root_element)
                                    else:
                                        break
                            except (RightJoinedStreamRanAhead, EndOfStreamError):
                                pass
                            except Exception:
                                logger.exception("Unhandled exception")

                        injected_kwargs = get_injected_kwargs(processing_func_type_hints, self._injector)
                        if current_key:
                            self._data_keys_to_send.add(current_key.key)
                        process_result = self._process_func(root_elements, *join_data_mappings, **injected_kwargs)
                        process_results, eos = _handle_result(process_result, process_results, eos)
                    else:
                        window_key = new_window_key
                        continue
                else:
                    injected_kwargs = get_injected_kwargs(processing_func_type_hints, self._injector)
                    if current_key:
                        self._data_keys_to_send.add(current_key.key)
                    process_result = self._process_func(root_user_element, *join_data_mapping, **injected_kwargs)
                    process_results, eos = _handle_result(process_result, process_results, eos)

            assert process_results or not self._return_type

            if self._return_type:
                for result in process_results:
                    self._output_broker.send(self._return_type, serializer(result))
                process_results.clear()
                self._broker.commit()
            if eos or self._eos:
                self._eos = True
                if self._return_type:
                    self._output_broker.send_eos(self._return_type)
                    self._broker.commit()
                return

    def save_results(self, data_key: DataKey, data: Union[StreamType, List[StreamType], None, EndOfStream]):
        if data:
            if isinstance(data, list):
                for data_item in data:
                    return_type = type(data_item)
                    local_serializer = self._serializers.get(return_type, _default_serializer)
                    self._output_broker.send(return_type, local_serializer(data_item))
            elif isinstance(data, EndOfStream):
                self._eos = True
                self._data_keys_to_send = {data_key.key}
            else:
                return_type = type(data)
                local_serializer = self._serializers.get(return_type, _default_serializer)
                self._output_broker.send(return_type, local_serializer(data))

        self._broker.commit(data_key)
        try:
            self._data_keys_to_send.remove(data_key.key)
        except KeyError:
            logger.exception(f'Failed to remove data key {data_key}')

        if not self._data_keys_to_send and self._eos:
            for explicit_return_type in self._explicit_return_types:
                self._output_broker.send_eos(explicit_return_type)

    def _get_joined_elements(
            self,
            join_node: JoinTreeNode,
            join_tree: JoinTree,
            left_element: dict,
            left_deserialized_element: StreamType,
            parent_children_map: Dict[StreamType, List[JoinedStreamType]],
    ):
        eos = False
        eos_exc = None
        for join_pair in get_tree_pairs(join_tree, join_node):
            right_join_node = join_pair.right_node
            left_expression = join_pair.left_expression
            right_expression = join_pair.right_expression

            try:
                for element_data in self._broker.get_elements(
                        right_join_node.user_type,
                        comparator=lambda right_element: compare_streams(left_expression(left_element), right_expression(right_element))
                ):
                    assert element_data is not None
                    deserialized_element = self._deserializers.get(right_join_node.user_type, _default_deserializer(right_join_node.user_type))(element_data)
                    parent_children_map.setdefault(left_deserialized_element, []).append(deserialized_element)

                    self._get_joined_elements(right_join_node, join_tree, element_data, deserialized_element, parent_children_map)
            except EndOfStreamError as exc:
                eos = True
                eos_exc = exc
                continue

        if eos:
            raise eos_exc


def _handle_result(process_result: Union[StreamType, StopIteration, None], process_results: list, eos: bool) -> Tuple[list, bool]:
    if not process_result or process_result is None:
        return process_results, eos

    if isinstance(process_result, StopIteration):
        return process_results, True

    if isinstance(process_result, Generator):
        for element in process_result:
            assert element
            if isinstance(element, StopIteration):
                return process_results, True
            process_results.append(element)
    else:
        process_results.append(process_result)
    return process_results, eos
