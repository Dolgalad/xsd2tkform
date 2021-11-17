"""XSD type definitions

XSDType class is the base class for all XSD types, inherited by the XSDSimpleType, XSDComplexType classes"""

from .element import Element, get_attributes
from .annotation import Annotation
from .restriction import Restriction
from .list import List
from .utils import get_annotation, get_restriction, get_list, get_sequence, get_extension

class XSDType:
    def __init__(self, name=None, annotation=None):
        self.name = name
        self.annotation = annotation
    def __eq__(self, e):
        if not isinstance(e, XSDType):
            return False
        return self.name==e.name and self.annotation==e.annotation
    def __str__(self):
        return "XSDType(name={})".format(self.name)

class SimpleType(XSDType):
    def __init__(self, name=None, restriction=None, item_list=None, attributes=[], *args, **kwargs):
        XSDType.__init__(self, name=name, *args, **kwargs)
        self.restriction=restriction
        self.item_list = item_list
        self.attributes=attributes
    def __eq__(self, e):
        if not isinstance(e, SimpleType):
            return False
        return super().__eq__(e) and self.restriction==e.restriction and self.item_list==e.item_list and self.attributes==e.attributes
    def __str__(self):
        att=["name={})".format(self.name)]
        if self.restriction is not None:
            att.append("\n\trestriction={}".format(str(self.restriction)))
        if self.item_list is not None:
            att.append("\n\tlist={}".format(self.item_list))
        if len(self.attributes):
            att.append("\n\tattributes={}".format(self.attributes))
        a = "SimpleType({}".format(", ".join(att))
        return a

class ComplexType(XSDType):
    def __init__(self, name=None, sequence=None, attributes=[], extension=None, *args, **kwargs):
        XSDType.__init__(self, name=name, *args, **kwargs)
        self.sequence=sequence
        self.attributes=attributes
        self.extension=extension
    def __eq__(self, e):
        if not isinstance(e, ComplexType):
            return False
        return super().__eq__(e) and self.sequence==e.sequence
    def __str__(self, tab_n=0):
        r = "ComplexType(name={})".format(self.name)
        if len(self.sequence):
            r+="\n"+self.sequence.__str__(tab_n=tab_n+1)
        if len(self.attributes):
            r+="\nAttributes {}".format(self.attributes)
        return r

class Group(XSDType):
    def __init__(self, name=None, sequence=None, *args, **kwargs):
        self.name = name
        self.sequence=sequence
    def __eq__(self, e):
        return super().__eq__(e) and self.name==e.name and self.sequence==e.sequence
    def __str__(self, tab_n=0):
        r="Group (name={})".format(self.name)
        if len(self.sequence):
            r += "\n"+self.sequence.__str__(tab_n=tab_n+1)
        return r


def from_element(element):
    """Parse a XML element to XSDType object
    """
    if "name" not in element.attrib:
        return
    name = element.attrib["name"]
    annotation = get_annotation(element)
    attributes = get_attributes(element)
    if element.tag.endswith("simpleType"):
        restriction = get_restriction(element)
        l= get_list(element)
        return SimpleType(name=name, annotation=annotation, restriction=restriction, item_list=l, attributes=attributes)
    elif element.tag.endswith("complexType"):
        sequence = get_sequence(element)
        extension = get_extension(element)
        if extension is None:
            return ComplexType(name, annotation=annotation, sequence=sequence, attributes=attributes)
        from .sequence import Sequence
        if isinstance(extension[1], Sequence):
            return ComplexType(name, annotation=annotation, sequence=sequence, attributes=attributes, extension=extension)
        if isinstance(extension[1], list):
            r=SimpleType(name, type=extensions[0], attributes=extension[1])
            return r
    elif element.tag.endswith("group"):
        sequence = get_sequence(element)
        return Group(name, annotation=annotation, sequence=sequence)
    elif element.tag.endswith("element"):
        e= Element.from_element(element)
        return e
    else:
        return None
