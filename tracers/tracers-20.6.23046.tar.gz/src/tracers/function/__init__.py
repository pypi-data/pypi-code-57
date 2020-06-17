# Standard library
import asyncio
import contextlib
import functools
import inspect
import time
import uuid
from contextvars import (
    ContextVar,
    Token,
)
from typing import (
    Callable,
    List,
    NamedTuple,
)

# Constants
CHAR_SPACE = chr(0x20)
CHAR_INFO = chr(0x1F6C8) + CHAR_SPACE
CHAR_CHECK_MARK = chr(0X2713)
CHAR_BROKEN_BAR = chr(0xA6)

# Containers
Frame = NamedTuple('Frame', [
    ('event', str),
    ('function', str),
    ('level', int),
    ('timestamp', float),
])

# Contextvars
DO_TRACE: ContextVar[bool] = ContextVar('DO_TRACE', default=True)
LEVEL: ContextVar[int] = ContextVar('LEVEL', default=0)
STACK: ContextVar[List[Frame]] = ContextVar('STACK', default=[])


def get_function_id(function: Callable, function_name: str = '') -> str:
    # Adding decorators to a function modify its metadata
    #   Fortunately functools' wrapped functions keep a reference to the parent
    while hasattr(function, '__wrapped__'):
        function = getattr(function, '__wrapped__')

    signature: str = '(...)'
    with contextlib.suppress(ValueError):
        signature = str(inspect.signature(function))

    module: str = function.__module__
    name: str = function_name or function.__name__
    prefix = 'async ' * asyncio.iscoroutinefunction(function)
    signature = signature if len(signature) < 48 else '(...)'

    if module not in {'__main__'}:
        return f'{prefix}{module}.{name}{signature}'

    return f'{prefix}{name}{signature}'


@contextlib.contextmanager
def increase_counter(contextvar):
    token: Token = contextvar.set(contextvar.get() + 1)
    try:
        yield
    finally:
        contextvar.reset(token)


def record_event(
    clock_id: int,
    event: str,
    function: Callable,
    function_name: str = '',
):
    STACK.get().append(Frame(
        event=event,
        function=get_function_id(function, function_name),
        level=LEVEL.get(),
        timestamp=time.clock_gettime(clock_id),
    ))


def analyze_stack(stack: List[Frame]):
    stack_levels: List[int] = [frame.level for frame in stack]

    total_time_seconds: float = \
        stack[-1].timestamp - stack[0].timestamp

    print()
    print(
        f'{CHAR_INFO} Finished transaction: {uuid.uuid4().hex}, '
        f'{total_time_seconds:.2f} seconds')
    print()
    print('  #    Timestamp      %     Total    Nested Call Chain')
    print()

    counter: int = 0
    for index, frame in enumerate(stack):
        indentation: str = (
            (CHAR_SPACE * 3 + CHAR_BROKEN_BAR) * (frame.level - 1)
            + (CHAR_SPACE * 3 + CHAR_CHECK_MARK)
        )

        if frame.event == 'call':
            counter += 1
            frame_childs: List[Frame] = \
                stack[index:stack_levels.index(frame.level, index + 1) + 1]

            relative_timestamp: float = \
                frame.timestamp - stack[0].timestamp

            raw_time_seconds: float = \
                frame_childs[-1].timestamp - frame_childs[0].timestamp

            raw_time_ratio: float = (
                100.0 * raw_time_seconds / total_time_seconds
                if total_time_seconds > 0.0
                else 100.0
            )

            print(
                f'{counter:>6} '
                f'{relative_timestamp:>8.2f}s '
                f'{raw_time_ratio:>5.1f}% '
                f'{raw_time_seconds:>8.2f}s '
                f'{indentation} '
                f'{frame.function}'
            )

    print()


def _get_wrapper(  # noqa: MC001
    *,
    clock_id: int = time.CLOCK_MONOTONIC,
    do_trace: bool = True,
    function_name: str = '',
    stack_analyzer: Callable[[List[Frame]], None] = analyze_stack,
) -> Callable:

    def decorator(function: Callable) -> Callable:

        if not do_trace or not DO_TRACE.get():

            # No overhead is introduced
            wrapper = function

            # Any downstream tracer is also disabled
            DO_TRACE.set(False)

        elif asyncio.iscoroutinefunction(function):

            @functools.wraps(function)
            async def wrapper(*args, **kwargs):
                if not LEVEL.get():
                    STACK.set([])

                with increase_counter(LEVEL):
                    record_event(clock_id, 'call', function, function_name)
                    result = await function(*args, **kwargs)
                    record_event(clock_id, 'return', function, function_name)

                if not LEVEL.get():
                    stack_analyzer(STACK.get())

                return result

        elif callable(function):

            @functools.wraps(function)
            def wrapper(*args, **kwargs):
                if not LEVEL.get():
                    STACK.set([])

                with increase_counter(LEVEL):
                    record_event(clock_id, 'call', function, function_name)
                    result = function(*args, **kwargs)
                    record_event(clock_id, 'return', function, function_name)

                if not LEVEL.get():
                    stack_analyzer(STACK.get())

                return result

        else:

            # We were not able to wrap this object
            wrapper = function

        return wrapper

    return decorator


def trace_process(
    *,
    do_trace: bool = True,
    function_name: str = '',
    stack_analyzer: Callable[[List[Frame]], None] = analyze_stack,
):
    return _get_wrapper(
        clock_id=time.CLOCK_PROCESS_CPUTIME_ID,
        do_trace=do_trace,
        function_name=function_name,
        stack_analyzer=stack_analyzer,
    )


def trace_thread(
    *,
    do_trace: bool = True,
    function_name: str = '',
    stack_analyzer: Callable[[List[Frame]], None] = analyze_stack,
):
    return _get_wrapper(
        clock_id=time.CLOCK_THREAD_CPUTIME_ID,
        do_trace=do_trace,
        function_name=function_name,
        stack_analyzer=stack_analyzer,
    )


def trace_monotonic(
    *,
    do_trace: bool = True,
    function_name: str = '',
    stack_analyzer: Callable[[List[Frame]], None] = analyze_stack,
):
    return _get_wrapper(
        clock_id=time.CLOCK_MONOTONIC,
        do_trace=do_trace,
        function_name=function_name,
        stack_analyzer=stack_analyzer,
    )


def trace(
    function: Callable = None,
    *,
    do_trace: bool = True,
    function_name: str = '',
    stack_analyzer: Callable[[List[Frame]], None] = analyze_stack,
):
    wrapper = trace_monotonic(
        do_trace=do_trace,
        function_name=function_name,
        stack_analyzer=stack_analyzer,
    )

    if function:
        return wrapper(function)

    return wrapper
