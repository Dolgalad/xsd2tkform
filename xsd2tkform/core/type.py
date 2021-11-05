"""XSD type definitions

XSDType class is the base class for all XSD types, inherited by the XSDSimpleType, XSDComplexType classes"""

from xsd2tkform.core.element import Element
from xsd2tkform.core.annotation import Annotation
from xsd2tkform.core.restriction import Restriction
from xsd2tkform.core.list import List
from xsd2tkform.core.utils import get_annotation, get_restriction, get_list, get_sequence

class XSDType:
    def __init__(self, name=None, annotation=None):
        self.name = name
        self.annotation = annotation
    def __str__(self):
        return "XSDType(name={})".format(self.name)

class SimpleType(XSDType):
    def __init__(self, name=None, restriction=None, item_list=None, *args, **kwargs):
        XSDType.__init__(self, name=name, *args, **kwargs)
        self.restriction=restriction
        self.item_list = item_list
    def __str__(self):
        att=["name={})".format(self.name)]
        if self.restriction is not None:
            att.append("\n\trestriction={}".format(str(self.restriction)))
        if self.item_list is not None:
            att.append("\n\tlist={}".format(self.item_list))
        a = "SimpleType({}".format(", ".join(att))
        return a

class ComplexType(XSDType):
    def __init__(self, name=None, sequence=None, *args, **kwargs):
        XSDType.__init__(self, name=name, *args, **kwargs)
        self.sequence=sequence
    def __str__(self, tab_n=0):
        r = "ComplexType(name={})".format(self.name)
        if len(self.sequence):
            r+="\n"+self.sequence.__str__(tab_n=tab_n+1)
        return r

class Group(XSDType):
    def __init__(self, name=None, sequence=None, *args, **kwargs):
        self.name = name
        self.sequence=sequence
    def __str__(self, tab_n=0):
        r="Group (name={})".format(self.name)
        if len(self.sequence):
            r += "\n"+self.sequence.__str__(tab_n=tab_n+1)
        return r


def from_element(element):
    """Parse a XML element to XSDType object
    """
    name = element.attrib["name"]
    annotation = get_annotation(element)
    if element.tag.endswith("simpleType"):
        restriction = get_restriction(element)
        l= get_list(element)
        return SimpleType(name=name, annotation=annotation, restriction=restriction, item_list=l)
    elif element.tag.endswith("complexType"):
        sequence = get_sequence(element)
        return ComplexType(name, annotation=annotation, sequence=sequence)
    elif element.tag.endswith("group"):
        sequence = get_sequence(element)
        return Group(name, annotation=annotation, sequence=sequence)
    elif element.tag.endswith("element"):
        return Element.from_element(element)
    else:
        return None
