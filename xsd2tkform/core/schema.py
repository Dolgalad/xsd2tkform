"""Schema definition
"""
from lxml import etree

from xsd2tkform.core.type import SimpleType, ComplexType, Group, from_element
from xsd2tkform.core.element import Element

class Schema:
    def __init__(self):
        self.items=[]
        self.simple_types={}
        self.complex_types={}
        self.groups={}
    def parse_element(self, element):
        td = from_element(element)
        if isinstance(td, SimpleType):
            self.simple_types[td.name]=td
        elif isinstance(td, ComplexType):
            self.complex_types[td.name]=td
        elif isinstance(td, Group):
            self.groups[td.name]=td
        elif isinstance(td, Element):
            self.items.append(td)
        else:
            print("Unknown type defined : ", element, element.attrib, element.tag)
    def get(self, typename):
        if ":" in typename:
            typename = typename.split(":")[-1]
        if typename in self.simple_types:
            return self.simple_types[typename]
        if typename in self.complex_types:
            return self.complex_types[typename]
        if typename in self.groups:
            return self.groups[typename]
    def __contains__(self, typename):
        if typename in self.simple_types:
            return True
        if typename in self.complex_types:
            return True
        if typename in self.groups:
            return True
        return False
 
    @staticmethod
    def from_element(element):
        if not element.tag.endswith("schema"):
            raise Exception("Cannot initialize Schema from {}".format(element))
        schema = Schema()
        # load type definitions and components
        for child in element:
            # ignore comments
            if isinstance(child, etree._Comment):
                continue
            schema.parse_element(child)
        return schema
    
