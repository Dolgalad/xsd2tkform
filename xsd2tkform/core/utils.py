from xsd2tkform.core.annotation import Annotation
from xsd2tkform.core.restriction import Restriction
from xsd2tkform.core.list import List
from xsd2tkform.core.sequence import Sequence
from xsd2tkform.core.choice import Choice
from xsd2tkform.core.element import Element

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
        if child.tag.endswith("sequence"):
            # children should be elements of choices
            for gchild in child:
                if gchild.tag.endswith("element"):
                    sequence.append(Element.from_element(gchild))
                elif gchild.tag.endswith("choice"):
                    sequence.append(Choice.from_element(gchild))
                else:
                    pass
    return Sequence(sequence)


