import inspect
import traceback


def sig(hub):
    pass


# TODO this needs to apply recursively to all grain functions
def call(hub, ctx):
    """
    Top level contract for grains collection
    """
    argspec = inspect.getfullargspec(ctx.func)
    kwargs = argspec.kwonlyargs
    if kwargs:
        raise ValueError(
            f"Grain collection functions do not take arguments: {', '.join(kwargs)}"
        )
    args = argspec.args[1:]
    if args:
        raise ValueError(
            f"Grain collection functions do not take arguments: {', '.join(args)}"
        )

    # TODO remove this try except from the init code once this contract can recursively be applied to all grain funcs
    try:
        return ctx.func(*ctx.args, **ctx.kwargs)
    except Exception as e:
        hub.log.critical(
            f"Exception raised while collecting grains:\n{traceback.format_exc()}"
        )
        if isinstance(e, AssertionError):
            # Assertion errors are deliberate, let them through
            raise


# These come from grains/init.py and the top level call shouldn't affect them
def call_release(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_release_all(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


async def call_wait_for(hub, ctx):
    return await ctx.func(*ctx.args, **ctx.kwargs)


def call_cli(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


def call_standalone(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


async def call_collect(hub, ctx):
    return await ctx.func(*ctx.args, **ctx.kwargs)


def call_run_sub(hub, ctx):
    return ctx.func(*ctx.args, **ctx.kwargs)


async def call_process_subs(hub, ctx):
    return await ctx.func(*ctx.args, **ctx.kwargs)


async def call_clean_value(hub, ctx) -> str or None:
    return await ctx.func(*ctx.args, **ctx.kwargs)
