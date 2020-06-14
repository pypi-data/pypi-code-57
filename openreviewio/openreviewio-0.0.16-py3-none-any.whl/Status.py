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

from datetime import datetime, timezone
from pathlib import Path
import toml


class Status:
    def __init__(
        self, value, author, date: str = datetime.now(timezone.utc).isoformat()
    ):
        """Status of a review.

        :param value: Value of the status. Accepted statuses are defined by the ORIO version. TODO: Insert here a dynamic list of available ones
        :param author: Author of the note.
        :param date: Note's time of creation, provided as ISO UTC (datetime.now(timezone.utc).isoformat()).
        """
        # Parameters
        status_allowed = toml.load(
            Path(__file__).parent.joinpath("orio_classes", "Status.toml")
        ).get("available")

        if value in status_allowed:
            self.state = value
        else:
            raise ValueError(
                f"Status '{value}' is not defined in the current version of OpenReviewIO standard."
                f"Available statuses are: {', '.join(status_allowed)}."
            )

        self.author = author
        self.date = date

    # TODO Override print for status to print: Status ... written by ... at ...
