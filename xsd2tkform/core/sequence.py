"""Sequence definition

"""

from .element import Element
from .choice import Choice

class Sequence:
    def __init__(self, items=[]):
        self.items = items
    def add(self, i):
        self.items.append(i)
    def __eq__(self, e):
        return self.items==e.items
    def __str__(self, tab_n=0):
        r="\t"*tab_n+"Sequence"
        if len(self.items):
            r+="\n"+"\n".join([i.__str__(tab_n=tab_n+1) for i in self.items])
        return r
    def __len__(self):
        return len(self.items)
    @staticmethod
    def from_element(element):
        if not element.tag.endswith("sequence"):
            raise Exception("Sequence::from_element : incompatible element")
        s=Sequence()
        # check the children
        for child in element:
            if child.tag.endswith("element"):
                s.add(Element.from_element(child))
            elif child.tag.endswith("choice"):
                s.add(Choice.from_element(child))
            elif child.tag.endswith("any"):
                s.add(AnyElement(**dict(child.attrib)))
            else:
                pass
        return s
