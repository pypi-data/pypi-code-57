"""
Module with classes describing an Object Oriented Programming object
"""
from xml.dom import minidom
from ._common_parser import parse_operation
from .class_member import Attribute


class Class:
    """
    Object Oriented Programming class object
    """

    def __init__(self, refid, name, stereotype=""):
        """
        Constructor

        :param refid: xml refid
        :param name: the Class name
        :type name: str
        :param sterotype: the Class stereotype
        :type stereotype: str
        """
        self.refid = refid
        self.name = name
        self.stereotype = stereotype
        self.generalization = []  # list of base classes
        self.attributes = []
        self.operations = []
        self.aggregation = []
        self.composition = []

    @classmethod
    def from_xml(cls, xml_file):
        clss = _parse_class_file(xml_file)
        return clss

    def add_attributes(self, att):
        """
        add attributes to the attribute list

        :param att: the attributes to add
        :type att: list
        """
        self.attributes.extend(att)

    def add_operations(self, op):
        """
        add operations to the operation list
        :param op: the attributes to add
        :type op: list
        """
        self.operations.extend(op)

    def add_generalizations(self, gens):
        """
        add generalizations to the generalization list

        :param op: the generalizations to add
        :type gens: list
        """
        self.generalization.extend(gens)

    def add_aggregations(self, agg):
        # self.aggregation = np.append(self.aggregation, agg)
        self.aggregation.extend(agg)

    def add_compositions(self, comp):
        self.composition.extend(comp)

    def to_string(self):
        """
        create a string for displaying the object

        :return: the object as a string
        :rtype: str
        """
        stereo = self.stereotype + " " if len(self.stereotype) > 0 else ""
        res = stereo + "Class " + self.name + "\n"

        res += "Generalization:\n"
        for g in self.generalization:
            res += "  " + g + "\n"

        res += "Aggregations:\n"
        for a in self.aggregation:
            print(a)
            res += "  " + a + "\n"

        res += "Composition:\n"
        for c in self.composition:
            res += "  " + c + "\n"

        res += "Attributes:\n"
        for a in self.attributes:
            res += "  "+a.to_string()+"\n"

        res += "Operations:\n"
        for o in self.operations:
            res += "  " + o.to_string()+"\n"

        return res

    def __str__(self):
        return self.to_string()


def _parse_attribute(member: minidom.Element):
    """
    Parse a xml element and create a Member class with it

    :param member: a xml element describing a class attribute (member)
    :return: a Attribute class object, a list of aggregations refid and a list of composition refid
    """

    mem_name = member.getElementsByTagName("name")[0].firstChild.nodeValue
    mem_privacy = member.getAttribute("prot")
    mem_type = ""

    aggreg = []
    compo = []
    for att_type in member.getElementsByTagName("type"):
        ref = att_type.getElementsByTagName("ref")
        if len(ref) > 0:
            ref = ref[0]
            mem_type = ref.firstChild.nodeValue
            if ref.hasAttribute("type"):
                if ref.getAttribute("type") in ["*","&","_ptr","pointer"]:
                    aggreg.append(ref.getAttribute("refid"))
            else:
                compo.append(ref.getAttribute("refid"))
        else:
            mem_type = att_type.firstChild.nodeValue

    res = Attribute(mem_name, mem_privacy, mem_type)
    brief_desc = ""
    desc = member.getElementsByTagName("briefdescription")
    if len(desc) > 0:
        desc = desc[0].getElementsByTagName("para")
        if len(desc) > 0:
            desc = desc[0].firstChild.nodeValue
            brief_desc = desc
    res.brief_desc = brief_desc
    return res, aggreg, compo


def _parse_class_file(file: str):
    """
    Parse a class xml file

    :param file: the file to parse
    :type file: str
    :return: an class object describing the parsed class
    """
    xml_doc = minidom.parse(file)

    compounddef = xml_doc.getElementsByTagName('compounddef')[0]
    refid = compounddef.attributes["id"].value

    class_name = compounddef.getElementsByTagName("compoundname")[0].firstChild.nodeValue
    obj_class = Class(refid, class_name)

    stereotype = ""
    kind = compounddef.attributes["kind"].value
    if kind in ["interface","protocol","exception"]:
        stereotype = kind
    if compounddef.hasAttribute("abstract"):
        if compounddef.attributes["abstract"].value == "yes":
            if len(stereotype) > 0:
                stereotype = "abstract "+stereotype
            else:
                stereotype = "abstract"

    obj_class.stereotype = stereotype

    gens = []
    basecompounds = compounddef.getElementsByTagName("basecompoundref")
    for cop in basecompounds:
        if cop.hasAttribute("refid"):
            gen_refid = cop.attributes["refid"].value
            gens.append(gen_refid)
    obj_class.add_generalizations(gens)

    sections = compounddef.getElementsByTagName("sectiondef")
    # print("nb section", len(sections))
    for section in sections:
        for member in section.getElementsByTagName("memberdef"):
            if member.attributes["kind"].value in ["property","variable"]:
                # print("  do_attribute",member.getElementsByTagName("name")[0].firstChild.nodeValue)
                att, agg, comp = _parse_attribute(member)
                obj_class.add_attributes([att])
                obj_class.add_aggregations(agg)
                obj_class.add_compositions(comp)
            elif member.attributes["kind"].value in ["event","function","signal","prototype","friend","slot"]:
                # print("  do_operation", member.getElementsByTagName("name")[0].firstChild.nodeValue)
                obj_class.add_operations([parse_operation(member)])

    return obj_class


if __name__ == '__main__':
    import os.path as opth

    doxyxml_root = opth.join(opth.dirname(__file__), "..")
    class_file = opth.join(doxyxml_root, "example_res/Doxygen/xml/class_geometry_1_1_rectangle.xml")
    print(opth.abspath(class_file))

    obj = Class.from_xml(class_file)
    print(obj)
    print(obj.refid)