# from typing import Callable, Type
# from functools import wraps
#
# from tokko_rpc.core.toolboxes import Toolbox
# from tokko_rpc.core.requests_x import Request, Header, Payload
#
#
# def cocoon(callback, headers: dict = None, **params):
#     headers = headers or {}
#     request = Request(headers=[Header(key=k, value=v) for k, v in headers.items()],
#                       payload=Payload(params=params),
#                       # request_id="pancho",
#                       # content_type="application/json-rpc",
#                       method="my-method")
#     print(request)
#     return callback
#
#
# def dispose_through_rpc(toolbox_class: Type[Toolbox] = Toolbox):
#     """ParasiteRPC decorator"""
#     def decorator(func: Callable):
#         @wraps(func)
#         def wrapper(self, *args, **kwargs):
#             return cocoon(func, *args, **kwargs)
#         setattr(toolbox_class, func.__name__, wrapper)
#         _meta = wrapper
#         _meta.__name__ = func.__name__
#         toolbox_class.Meta.add_field(_meta)
#         return func
#     return decorator
#
#
