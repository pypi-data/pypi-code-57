from inspect import signature, Parameter
from functools import wraps

from fastapi import Request, Header

def _param_kind_key(p):
    if p == Parameter.POSITIONAL_ONLY:
        return 1
    elif p == Parameter.POSITIONAL_OR_KEYWORD:
        return 2
    elif p == Parameter.KEYWORD_ONLY:
        return 3
    elif p == Parameter.VAR_POSITIONAL:
        return 4
    else:
        return 5

def adimap(pre = None, post = None):
    def intercept(body):
        body_sig          = signature(body)
        merged_parameters = list(body_sig.parameters.values())

        if pre is not None:
            pre_sig = signature(pre)

            for p0 in pre_sig.parameters.values():
                p1 = next((p1 for p1 in merged_parameters if p0.name == p1.name), None)

                if p1 is not None:
                    if p0.annotation != p1.annotation:
                        raise ValueError("conflict parameters")
                else:
                    merged_parameters.append(p0)

        merged_parameters.sort(key=_param_kind_key)

        handle_sig = body_sig.replace(parameters=merged_parameters)

        @wraps(body)
        async def handle(**kwargs):
            if pre is not None:
                pre_kwargs = { k : kwargs[k] for k in pre_sig.parameters }
                ret = await pre(**pre_kwargs)

            if ret is not None:
                return ret

            body_kwargs = { k : kwargs[k] for k in body_sig.parameters }

            ret = await body(**body_kwargs)

            if post is not None:
                return await post(ret)

            return ret

        handle.__signature__ = handle_sig

        return handle

    return intercept
