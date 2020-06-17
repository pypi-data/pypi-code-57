import abc


class Member(metaclass=abc.ABCMeta):
    """
    Abstract Class Member
    """

    def __init__(self, name, privacy, typ):
        """
        Constructor
        :param name: the member name
        :type name: str
        :param privacy: the member privacy
        :type privacy: str (public, private or protected)
        :param typ: the member type
        :type typ: str
        """

        assert(privacy in ["public", "private",  "protected" ])

        self.name = name
        self.privacy = privacy
        self.type = typ
        self.brief_desc = ""
        self._xrefsect = []  # xref sections for custom doxygen tags

        self.header_location = ""  # header file location
        self.body_location = ""  # cpp file location

    @property
    def xrefsect(self):
        return self._xrefsect

    @abc.abstractmethod
    def to_string(self):
        """
        create a string for displaying the object
        :return: the object as a string
        :rtype: str
        """
        return ""


class Attribute(Member):
    """
    Class attribute
    """

    def __init__(self, name: str, privacy: str, typ: str):
        """
        Constructor
        :param name: the attribute name
        :type name: str
        :param privacy: the attribute privacy
        :type privacy: str
        :param typ: the attribute type
        :type typ: str
        """

        Member.__init__(self, name, privacy,typ)

    def to_string(self):
        """
        create a string for displaying the object
        :return: the object as a string
        :rtype: str
        """
        res = "  " + self.privacy + " " + self.type + " " + self.name
        return res


class Operation(Member):
    """
    Class operation
    """

    def __init__(self, name, privacy, retType, args):
        """

        :param name: the operation name
        :type name: str
        :param privacy: the operation privacy
        :type privacy: str
        :param retType: the return type
        :type retType: str
        :param args: the operation arguments
        :type args: list[str]
        """

        Member.__init__(self, name, privacy, retType)
        self.arguments = args

    def to_string(self):
        """
        create a string for displaying the object
        :return: the object as a string
        :rtype: str
        """
        res = "  " + self.privacy + " " + self.type + " " + self.name +"("+", ".join(self.arguments)+")"
        for sec in self.xrefsect:
            if sec.title == "task":
                res += " task: " + sec.description
        return res


class XRefSect:
    """
    class to describe xrefsect doxygen tags
    """
    def __init__(self, in_id, title, desc):
        self._id = in_id
        self._title = title
        self._description = desc

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    def __str__(self):
        return self._title + " " + self._description