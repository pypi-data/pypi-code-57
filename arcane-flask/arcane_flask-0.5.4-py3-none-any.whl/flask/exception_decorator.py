import functools
import inspect
import traceback
from typing import Callable

from .authentication import get_user_email
from arcane.pubsub import pubsub_message_decoder


def catch_exceptions_service(service: str, pubsub_subscriber: bool=False) -> Callable:
    """ Catch if an exception is raised after an endpoint call and alert it with arguments or parameters (pubsub case)
        passed to this endpoint
    """
    def catch_exceptions(job_func: Callable) -> Callable:
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            if pubsub_subscriber:
                try:
                    job_func_signature = inspect.signature(job_func)
                    message_kw = list(job_func_signature.parameters.keys())[0]
                    message_data = kwargs[message_kw]['message']['data']
                    decoded_pay_load = pubsub_message_decoder(message_data)
                    parameters = decoded_pay_load['parameters']
                except (KeyError, ValueError, IndexError, TypeError):
                    parameters = kwargs
            try:
                return job_func(*args, **kwargs)
            except Exception as e:
                message = f"Error while executing method {job_func.__name__} in service {service} with parameters "
                if pubsub_subscriber:
                    message += f'{parameters}'
                else:
                    message += f"args : {str(args)} / kwargs : {str(kwargs)}"
                try:
                    message += f' for user {get_user_email()}'
                except ValueError:
                    pass
                traceback_str = traceback.format_exc()
                print(f"{traceback_str}\n{message}")
                raise e
        return wrapper
    return catch_exceptions
