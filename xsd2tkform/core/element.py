"""Element definition
"""
from lxml import etree

class Attribute:
    def __init__(self, name=None, type="string", use=None, default=None):
        self.name=name
        self.type=type
        self.use=use
        self.default=default
    def mandatory(self):
        return self.use=="required"
    def __eq__(self, e):
        if not isinstance(e, Attribute):
            return False
        return self.name==e.name and self.type==e.type and self.use==e.use and self.default==e.default
    def __str__(self):
        return "Attribute (name={}, type={}, use={}, default={})".format(self.name, self.type, self.use, self.default)
    @staticmethod
    def from_element(element):
        att=dict(element.attrib)
        return Attribute(**att)

class AnyElement:
    def __init__(self, **kwargs):
        self.attributes=kwargs
    def __str__(self, *args, **kwargs):
        return "AnyElement"

class Element:
    def __init__(self, name=None, etype=None, min_occurs=1, max_occurs=1, abstract=False, typedef=None, ref=None, substitution_group=None,**kwargs):
        self.name=name
        self.type=etype
        self.min_occurs=min_occurs
        self.max_occurs=max_occurs
        self.typedef = typedef
        self.abstract=abstract
        self.ref=ref
        self.substitution_group=substitution_group
        if self.type is None:
            if self.typedef is None:
                self.type = self.name
            else:
                self.type = self.typedef.name
    def __eq__(self, e):
        return self.name==e.name and self.type==e.type and self.min_occurs==e.min_occurs and \
                self.max_occurs==e.max_occurs and self.typedef==e.typedef and self.abstract==e.abstract and \
                self.ref==e.ref and self.substitution_group==e.substitution_group
    def __str__(self, tab_n=0):
        return "\t"*tab_n+"Element(name={}, type={}, min_occurs={}, max_occurs={}, abstract={}, typedef={}, ref={})".format(self.name, 
                self.type,self.min_occurs, self.max_occurs, self.abstract, self.typedef, self.ref)
    @staticmethod
    def from_element(element):
        att=dict(element.attrib)
        if "type" in att:
            att["etype"]=att.pop("type")
        if "minOccurs" in att:
            att["min_occurs"]=att.pop("minOccurs")
            if att["min_occurs"].isdigit():
                att["min_occurs"]=int(att["min_occurs"])
        if "maxOccurs" in att:
            att["max_occurs"]=att.pop("maxOccurs")
            if att["max_occurs"].isdigit():
                att["max_occurs"]=int(att["max_occurs"])
        if "substitutionGroup" in att:
            att["substitution_group"]=att.pop("substitutionGroup")
        if "abstract" in att:
            print("ABSTRACT val ", att["abstract"], type(att["abstract"]))
            if att["abstract"]=="true":
                att["abstract"]=True
            if att["abstract"]=="false":
                att["abstract"]=False
        # check if element contains type definition
        ct=None
        for child in element:
            if child.tag.endswith("complexType"):
                from .type import ComplexType, SimpleType
                from .utils import get_sequence, get_extension
                from .sequence import Sequence
                sequence = get_sequence(child)
                attributes= get_attributes(child)
                extension=get_extension(child)
                if extension is None:
                    ct=ComplexType(att["name"], annotation=None, sequence=sequence, attributes=attributes, extension=extension)
                elif isinstance(extension[1], Sequence):
                    ct=ComplexType(att["name"], annotation=None, sequence=sequence, attributes=attributes, extension=extension)
                elif isinstance(extension[1], list):
                    from .restriction import Restriction
                    ct=SimpleType(att["name"], restriction=Restriction(base=extension[0]), attributes=extension[1])
                else:
                    ct=ComplexType(att["name"], annotation=None, sequence=sequence, attributes=attributes, extension=extension)
                continue



        return Element(typedef = ct, **att)

def get_attributes(element):
    attributes=[]
    for child in element:
        if isinstance(child, etree._Comment):
            continue
        if child.tag.endswith("}attribute"):
            attributes.append(Attribute.from_element(child))
    return attributes
