"""Choice definition
"""

from .element import Element

class Choice:
    def __init__(self, min_occurs=0, max_occurs=0):
        self.min_occurs=min_occurs
        self.max_occurs=max_occurs
        self.elements=[]
    def add(self, i):
        self.elements.append(i)
    def __str__(self, tab_n=0):
        r="\t"*tab_n + "Choice (min_occurs={}, max_occurs={})".format(self.min_occurs, self.max_occurs)
        if len(self.elements):
            r+="\n"+"\n".join([i.__str__(tab_n=tab_n+1) for i in self.elements])
        return r
    @staticmethod
    def from_element(element):
        if not element.tag.endswith("choice"):
            raise Exception("Initializing Choice object from element {}".format(element))
        att=element.attrib
        if "minOccurs" in att:
            att["min_occurs"]=att.pop("minOccurs")
        if "maxOccurs" in att:
            att["max_occurs"]=att.pop("maxOccurs")
        c=Choice(**att)
        if not element.tag.endswith("choice"):
            pass
        for child in element:
            c.add(Element.from_element(child))
        return c
