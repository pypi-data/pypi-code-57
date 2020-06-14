# This file is part of openreviewio-py.
#
# openreviewio-py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# openreviewio-py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with openreviewio-py.  If not, see <https://www.gnu.org/licenses/>


from __future__ import annotations
from typing import List, Union
from datetime import datetime, timezone
from .Content import Content


class Note:
    def __init__(
        self,
        author: str,
        date: str = "",
        contents: Union[Content, List[Content]] = None,
        parent: Note = None,
    ):
        """Contains contents.

        :param author: Author of the note.
        :param date: Note's time of creation, provided as ISO UTC (datetime.now(timezone.utc).isoformat()).
        :param contents: All note's contents. You can pass a single content at construction.
        :param parent: Note to reply to.
        """
        self.author = author
        self.date = date or datetime.now(timezone.utc).isoformat()

        self.contents = []
        if contents:
            self.add_content(contents)

        self.parent = parent

    def add_content(self, content: Union[Content, List[Content]]):
        """Add content to the note.
        If the content is an Abstract one, a TypeError is raised.

        :param content: Content to add to the note.
        :return: Created content."""

        # Sentinel for checking if content type is valid
        if getattr(content, "__type__", "") == "Abstract":
            raise TypeError(
                f"Cannot create content from {content.__name__}, it is an abstract type."
            )

        # Add content, if list add all of them by running this function for each element to have the Abstract check
        if type(content) is list:
            for a in content:
                self.add_content(a)
        else:
            self.contents.append(content)
