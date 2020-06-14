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

from typing import Union
from pathlib import Path
from .Content import Content
from .Note import Note
from .Status import Status
from .MediaReview import MediaReview


def load_media_review(media_review_path: Union[str, Path]) -> MediaReview:
    """Build a MediaReview object from the written media review at the given path.

    :param media_review_path: Path of written media review to load.
    :return: MediaReview object.
    """
    media_review_path = Path(media_review_path)

    if media_review_path.is_dir():
        review_folder_root = media_review_path
    else:
        review_folder_root = media_review_path.parent

    review_file = review_folder_root.joinpath("review.orio")

    # Build Review
    import xml.etree.ElementTree as ET

    review_xml = ET.parse(review_file).getroot()

    review = MediaReview(review_xml.attrib.get("media_path"))

    #   Statuses
    # Build statuses list
    statuses = []
    for status in review_xml.find("statuses").iter("status"):
        status_attributes = status.attrib
        statuses.append(
            Status(
                date=status_attributes.get("date"),
                author=status_attributes.get("author"),
                value=status.text,
            )
        )

    current_status = statuses[-1]

    # Set statuses to review
    review.set_status_history(statuses)
    review.status = current_status

    # Notes
    for n in review_xml.find("notes").iter("note"):
        note_attributes = n.attrib
        parent_note = review.get_note(note_attributes.get("parent", None))
        note = Note(
            author=note_attributes.get("author"),
            date=note_attributes.get("date"),
            parent=parent_note,
        )

        # Contents
        contents = []
        for a in n.find("contents").iter():
            if a.attrib:
                content = getattr(Content, a.tag)(**a.attrib)
                contents.append(content)

        note.contents = contents

        review.add_note(note)

    return review
