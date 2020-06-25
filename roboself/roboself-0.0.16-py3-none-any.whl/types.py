from types import SimpleNamespace

from roboself.chat import Chat
from roboself.graph import Graph

ROBOSELF_TYPE_ATTR = "_roboself_type"
ROBOSELF_ACTION_VALUE = "action"


class ActionContext(SimpleNamespace):
    """The context that is passed to an action as the first parameter."""
    intent_name: str

    chat: Chat
    kb: Graph

    # TODO: activate these one by one
    # progress: Progress
    # context: Context
    # user: User
