from types import SimpleNamespace

from roboself.chat import Chat

ROBOSELF_TYPE_ATTR = "_roboself_type"
ROBOSELF_ACTION_VALUE = "action"


class ActionContext(SimpleNamespace):
    """The context that is passed to an action as the first parameter."""
    intent_name: str

    chat: Chat

    # TODO: activate these one by one
    # kb: Graph
    # progress: Progress
    # context: Context
    # user: User
