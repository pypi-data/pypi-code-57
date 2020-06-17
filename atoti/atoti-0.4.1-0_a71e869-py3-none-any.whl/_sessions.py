"""Sessions."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from types import TracebackType
from typing import Any, Dict, MutableMapping, Optional, Type, Union

from ._ipython_utils import ipython_key_completions_for_mapping
from ._repr_utils import ReprJson, convert_repr_json_to_html
from .config import SessionConfiguration, _get_merged_config
from .session import Session


@dataclass(frozen=True)
class Sessions(MutableMapping[str, Session]):
    """Manage the sessions."""

    _sessions: Dict[str, Session] = field(default_factory=dict)

    def create_session(
        self,
        name: str = "Unnamed",
        *,
        config: Optional[Union[SessionConfiguration, Path, str]] = None,
        **kwargs: Any,
    ) -> Session:
        """Create a session.

        Args:
            name: The name of the session.
            config: The configuration of the session or the path to a configuration file.
        """
        merged_config = _get_merged_config(config)
        full_config = (
            merged_config._complete_with_default()  # pylint: disable=protected-access
        )
        if name in self._sessions:
            logging.getLogger("atoti.session").warning(
                """Deleting existing "%s" session to create the new one.""", name
            )
            del self[name]
        self[name] = Session(
            name,
            config=full_config,
            # We use kwargs to hide uncommon features from the public API.
            **kwargs,
        )
        return self._sessions[name]

    def __enter__(self) -> Sessions:
        """Enter this sessions manager's context manager.

        Returns:
            ourself to assign it to the "as" keyword.

        """
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Exit this sessions' context manager.

        Close all the managed sessions.

        """
        self.close()

    def close(self):
        """Close all the managed sessions."""
        for session in self._sessions.values():
            session.close()

    def _get_session_as_json(self, name: str) -> str:
        """Return a JSON string used by the JupyterLab extension to connect to a session."""
        session = self[name]
        return json.dumps(
            {
                "port": session.port,
                "token": session._generate_token(),  # pylint: disable= protected-access
                "url": session.url,
            }
        )

    def _remove_closed_sessions(self) -> None:
        sessions_to_remove = [
            session for session in self._sessions.values() if session.closed
        ]
        for session in sessions_to_remove:
            del self._sessions[session.name]

    def __setitem__(self, key: str, value: Session) -> None:
        """Add a session."""
        self._remove_closed_sessions()
        if key in self._sessions:
            del self[key]
        self._sessions[key] = value

    def __getitem__(self, key: str) -> Session:
        """Get a session."""
        self._remove_closed_sessions()
        return self._sessions[key]

    def __delitem__(self, key: str) -> None:
        """Remove a session.

        This method also stops the Java session, destroying all Java objects attached to it.
        """
        self._remove_closed_sessions()
        if key in self._sessions:
            session = self._sessions[key]
            session.close()
            del self._sessions[key]

    def __iter__(self):
        """Return the iterator on sessions."""
        return iter(self._sessions)

    def __len__(self) -> int:
        """Return the number of sessions."""
        return len(self._sessions)

    def _ipython_key_completions_(self):
        return ipython_key_completions_for_mapping(self)

    def _repr_html_(self):
        return convert_repr_json_to_html(self)

    def _repr_json_(self) -> ReprJson:
        return (
            {
                name: session._repr_json_()[0]
                for name, session in sorted(self._sessions.items())
            },
            {"root": "Sessions", "expanded": False},
        )
