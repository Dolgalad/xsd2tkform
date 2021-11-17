"""Schema definition
"""
from lxml import etree

from .type import SimpleType, ComplexType, Group, from_element
from .element import Element

class Schema:
    def __init__(self, filename):
        self.filename=filename # need filename to manage include statements
        self.root_items = []
        self.items=[]
        #self.elements={} # map element names to their type
        self.simple_types={}
        self.complex_types={}
        self.groups={}
    def find_ref(self, name):
        for i in self.items:
            if i.name==name:
                return i
    def find_substitutions(self, name):
        return [e for e in self.items if e.substitution_group==name]
    def include_schema(self, element):
        schema_file = element.attrib["schemaLocation"]
        from .parser import XSDParser
        import os
        path = os.path.join(os.path.dirname(self.filename), schema_file)
        parser = XSDParser(path)
        for schema in parser.schemas:
            self.add_schema(schema)
    def add_schema(self, schema):
        for i in schema.items:
            if not i in self.items:
                self.items.append(i)
        for ri in schema.root_items:
            if not ri in self.root_items:
                self.root_items.append(ri)
        # simple types
        for k in schema.simple_types:
            self.simple_types[k]=schema.simple_types[k]
        # complex types
        for k in schema.complex_types:
            self.complex_types[k]=schema.complex_types[k]
        # groups
        for k in schema.groups:
            self.groups[k]=schema.groups[k]



    def parse_element(self, element, root=True, name=None):
        # if element is an include statement
        if element.tag.endswith("}include"):
            self.include_schema(element)
        td = from_element(element)
        if td is not None:
            if td.name=="get":
                pass
        if isinstance(td, SimpleType):
            self.simple_types[td.name]=td
        elif isinstance(td, ComplexType):
            self.complex_types[td.name]=td
        elif isinstance(td, Group):
            self.groups[td.name]=td
        
        elif isinstance(td, Element):
            if td.type is None:
                # get type definition in this element
                td.type=td.name
                ct = td.typedef
                self.complex_types[ct.name]=ct
                #for child in element:
                #    self.parse_element(child, name=td.name, root=False)
                #td.type = td.name

            self.items.append(td)
            if root:
                self.root_items.append(td)
        else:
            pass

        # WARNING : should not do this
        for child in element:
            if isinstance(child, etree._Comment):
                continue
            self.parse_element(child, root=False)
    def apply_substitutions(self):
        for i in self.items:
            if i.substitution_group is not None:
                # get the current object type definition
                td = self.get(i.type)
                # get the base type
                bases = [e for e in self.items if e.name==i.substitution_group]
                if len(bases):
                    # get the corresponding type
                    base_t = self.get(bases[0].type)
                    for att in base_t.attributes:
                        if not att in td.attributes:
                            td.attributes.append(att)
                    self.complex_types[td.name]=td
    def apply_extensions(self):
        for k in self.complex_types:
            t = self.complex_types[k]
            if t.extension is not None:
                # get base type
                base_type = self.get(t.extension[0])
                # add attributes and sequence element
                for att in base_type.attributes:
                    if not att in t.attributes:
                        t.attributes.append(att)
                for item in base_type.sequence.items:
                    if not item in t.sequence.items:
                        t.sequence.add(item)
                t.sequence = t.extension[1]
                t.extension=None
    def get(self, typename):
        if ":" in typename:
            typename = typename.split(":")[-1]
        if typename in self.simple_types:
            return self.simple_types[typename]
        if typename in self.complex_types:
            return self.complex_types[typename]
        if typename in self.groups:
            return self.groups[typename]
        for item in self.items:
            if typename==item.name:
                return item
    
    def __contains__(self, typename):
        if typename in self.simple_types:
            return True
        if typename in self.complex_types:
            return True
        if typename in self.groups:
            return True
        item_names = [i.name for i in self.items]
        if typename in item_names:
            return True
        return False
 
    @staticmethod
    def from_element(element, filename):
        if not element.tag.endswith("schema"):
            raise Exception("Cannot initialize Schema from {}".format(element))
        schema = Schema(filename=filename)
        # load type definitions and components
        for child in element:
            # ignore comments
            if isinstance(child, etree._Comment):
                continue
            schema.parse_element(child)
        return schema
    
