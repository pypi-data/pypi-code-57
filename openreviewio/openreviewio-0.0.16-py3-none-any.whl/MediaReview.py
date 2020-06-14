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
from pathlib import Path
import shutil
import operator
from typing import List, Union
from .Status import Status
from .Note import Note
from .Content import Content
import xml.etree.ElementTree as ET


class MediaReview:

    media: Path
    _status_history: List[Status] = []  # Read only

    def __init__(
        self, media: Union[str, Path], status: Status = None, notes: List[Note] = None,
    ):
        """Review of a media.

        :param media: Path to the media the review is linked to.
        :param status: Review status.
        :param notes: Review's notes ordered by creation date. TODO Read only ?
        """
        self.media = Path(media)

        self.status = status or Status("waiting review", "")

        self._status_history = []
        self._status_history.append(self.status)

        self.notes = []
        if notes:
            self.add_note(notes)

    def add_note(self, note: Union[Note, List[Note]] = None):
        """Append a note (or all notes if a list is provided) it to the review's notes list.

        :param note: Note(s) to add."""

        if type(note) is list:
            for n in note:
                self.add_note(n)
        else:
            # Append note to notes if there is no note with the same date
            if note.date not in [n.date for n in self.notes]:
                self.notes.append(note)

        # Sort notes by date
        self.notes = sorted(self.notes, key=operator.attrgetter("date"))

    def get_note(self, date: str) -> Note:
        """Get a note by it's date.

        :return: Note
        """
        for n in self.notes:
            if n.date == date:
                return n

    def write(
        self, path: Union[str, Path] = "", include_attached_files: bool = True
    ) -> Path:
        """Write the review in a folder according to the folder structure.
        If no path provided, the note is written next to the related media file in a folder 'media_name.ext.orio'.

        :param path: Folder path to write the review.
        :param include_attached_files: Copies all files related to contents in the created folder.
        :return: Path to the folder of the exported media review.
        """
        # Create review
        from inspect import getmembers

        path = Path(path)

        if not path.is_dir():
            raise ValueError("Writing path target must be a folder.")

        if path.suffix == ".orio":
            review_folder = path
        else:
            review_folder = path.joinpath(f"{self.media.name}.orio")

        # XML
        # create the file structure
        review = ET.Element(
            "review",
            {
                "media_path": str(self.media),
                "media_signature": "d41d8cd98f00b204e9800998ecf8427e",
            },
        )

        # Statuses
        statuses = ET.SubElement(review, "statuses")
        for s in self.get_status_history():
            status = ET.Element("status", {"date": s.date, "author": s.author})
            status.text = s.state
            statuses.append(status)

        # Notes
        notes = ET.SubElement(review, "notes")
        files_to_copy = []
        for n in self.notes:
            note = ET.Element(
                "note",
                {
                    "date": n.date,
                    "author": n.author,
                    "parent": n.parent.date if n.parent else "",
                },
            )

            # Contents
            contents = ET.SubElement(note, "contents")
            for c in n.contents:
                # Dynamically set parameters from members
                params = {}
                for attribute, value in getmembers(c):
                    if not attribute.startswith("__"):
                        if attribute == "path_to_image":
                            if include_attached_files:
                                # Set path_to_image as relative
                                relative_path = Path(
                                    n.date.replace(":", "_"), Path(value).name
                                )
                                params["path_to_image"] = str(relative_path)
                                # Keep files to copy
                                files_to_copy.append(
                                    (Path(value), review_folder.joinpath(relative_path))
                                )
                                # Update attribute of written note
                                setattr(c, attribute, relative_path)
                        else:
                            params[attribute] = str(value)
                content = ET.Element(c.__class__.__name__, params)
                contents.append(content)

            ET.SubElement(note, "metadata")
            notes.append(note)

        #   Write to folder
        if not review_folder.is_dir():
            review_folder.mkdir()

        # Write to file
        # create a new XML file with the results
        from xml.dom import minidom

        xmlstr = minidom.parseString(ET.tostring(review, encoding="utf-8")).toprettyxml(
            indent="   "
        )
        file = review_folder.joinpath("review.orio")
        with file.open("w") as f:
            f.write(xmlstr)

        # Copy files if there have to be copied
        for source, target in files_to_copy:
            if not target.parent.is_dir():
                target.parent.mkdir()

            if not target.is_file():
                shutil.copy2(source, target)

    def compare(self, review: MediaReview) -> MediaReview:
        """Compare the current review with the given one.
        TODO: Not implemented yet!

        :returns: A differential review with notes included in the current review that they aren't in the compared one.
        """
        pass

    def get_status_history(self) -> List[Status]:
        """Give the statuses history of the review.

        :returns: A list of statuses
        """
        return self._status_history

    def set_status_history(self, statuses_list):
        """Set the statuses history of the review.
        """
        self._status_history = statuses_list
