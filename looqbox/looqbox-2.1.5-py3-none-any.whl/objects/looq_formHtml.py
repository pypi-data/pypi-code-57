import json
from looqbox.objects.looq_object import LooqObject
from collections import OrderedDict


class ObjFormHTML(LooqObject):
    """
    Creates a Looqbox form HTML object.

    Attributes:
    --------
        :param html: HTML string to be executed.
        :param str filepath: Form input file path.
        :param str content: Form content.

    Example:
    --------

    Properties:
    --------
        to_json_structure()
            :return: A JSON string.
    """

    def __init__(self, filepath=None, html=None, content=[]):
        """
        Creates a view to drag and drop a file that will be read and used in other script of the response.

        Parameters:
        --------
            :param html: HTML string to be executed.
            :param str filepath: Form input file path.
            :param str content: Form content.

        Example:
        --------
        """
        super().__init__()
        self.html = html
        self.filepath = filepath
        self.content = content

    @property
    def to_json_structure(self):
        """
        Creates the JSON structure to be read by the FES.

        :return: A JSON string.
        """
        json_content = OrderedDict(
            {
                "objectType": "formHtml",
                "html": self.html,
                "content": self.content,
                "filepath": self.filepath,
            }
        )

        # Transforming in JSON
        form_json = json.dumps(json_content, indent=1)

        return form_json
