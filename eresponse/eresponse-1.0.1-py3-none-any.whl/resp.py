from eresponse.models import ErrorMessage, SuccessMessage


def new_error_message(message):
    message = ErrorMessage(message)
    return message.to_json()


def new_success_message(message=None, **kwargs):
    message = SuccessMessage(message, **kwargs)
    return message.to_json()
