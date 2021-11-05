"""Element definition
"""

class Element:
    def __init__(self, name=None, etype=None, min_occurs=0, max_occurs=0):
        self.name=name
        self.type=etype
        self.min_occurs=min_occurs
        self.max_occurs=max_occurs
    def __str__(self, tab_n=0):
        return "\t"*tab_n+"Element(name={}, type={}, min_occurs={}, max_occurs={})".format(self.name, 
                self.type,self.min_occurs, self.max_occurs)
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
        return Element(**att)
