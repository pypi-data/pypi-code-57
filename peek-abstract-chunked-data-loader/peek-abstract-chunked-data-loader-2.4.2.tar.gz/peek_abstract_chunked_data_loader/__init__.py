
from peek_plugin_base.server.PluginServerEntryHookABC import PluginServerEntryHookABC
from peek_plugin_base.client.PluginClientEntryHookABC import PluginClientEntryHookABC
from peek_plugin_base.agent.PluginAgentEntryHookABC import PluginAgentEntryHookABC
from typing import Type

__version__ = '2.4.2'


def peekServerEntryHook() -> Type[PluginServerEntryHookABC]:
    from .private.server.ServerEntryHook import ServerEntryHook
    return ServerEntryHook


def peekAgentEntryHook() -> Type[PluginAgentEntryHookABC]:
    from .private.agent.AgentEntryHook import AgentEntryHook
    return AgentEntryHook
