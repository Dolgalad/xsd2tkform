from lxml import etree

from .annotation import Annotation
from .restriction import Restriction
from .list import List
from .sequence import Sequence
from .choice import Choice
from .element import Element, AnyElement

def get_annotation(element):
    """Get annotations from a type definition element
    """
    docs={}
    for child in element:
        if child.tag.endswith("annotation"):
            for gchild in child:
                if gchild.tag.endswith("documentation"):
                    # find language
                    for k in gchild.attrib:
                        if k.endswith("lang"):
                            docs[gchild.attrib[k]]=gchild.text.strip()
    return Annotation(docs=docs)
def get_restriction(element):
    for child in element:
        if child.tag.endswith("restriction"):
            if len(child):
                enum=[e.attrib["value"] for e in child if e.tag.endswith("enumeration")]
                return Restriction(base=child.attrib["base"], enum=enum)
            else:
                return Restriction(base=child.attrib["base"])
    return
def get_list(element):
    item_list=None
    for child in element:
        if child.tag.endswith("list"):
            attr = child.attrib
            attr["item_type"]=attr.pop("itemType")
            item_list=List(**attr)
    return item_list

def get_sequence(element):
    sequence = []
    for child in element:
        if isinstance(child, etree._Comment):
            continue
        if child.tag.endswith("sequence"):
            # children should be elements of choices
            for gchild in child:
                if gchild.tag.endswith("element"):
                    sequence.append(Element.from_element(gchild))
                elif gchild.tag.endswith("choice"):
                    sequence.append(Choice.from_element(gchild))
                elif gchild.tag.endswith("any"):
                    sequence.append(AnyElement(**dict(gchild.attrib)))
                else:
                    pass
    return Sequence(sequence)

def get_extension(element):
    from .element import get_attributes
    for child in element:
        if isinstance(child, etree._Comment):
            continue
        if child.tag.endswith("}complexContent"):
            # extension
            if child[0].tag.endswith("}extension"):
                base_type = child[0].attrib["base"]
                sequence = get_sequence(child[0])
                return (base_type, sequence)
        if child.tag.endswith("}simpleContent"):
            # extension
            if child[0].tag.endswith("}extension"):
                base_type = child[0].attrib["base"].split(":")[-1]
                attributes = get_attributes(child[0])
                return (base_type, attributes)

    return None
