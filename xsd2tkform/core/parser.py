"""XSD schema parser

For now we suppose the file contains a single schema
"""
from lxml import etree

from .type import SimpleType, ComplexType, Group, from_element
from .annotation import Annotation
from .schema import Schema

class XSDParser:
    def __init__(self, filename=None):
        # initialize type definition storage
        self.schemas=[]

        # if filename was passed as argument
        self.parse(filename)
    def parse(self, filename):
        tree = etree.parse(filename)
        root = tree.getroot()
        ns=root.nsmap
        # if root is a schema
        if root.tag.endswith("schema"):
            self.schemas.append(Schema.from_element(root, filename))
            # apply substitutions
            self.schemas[-1].apply_substitutions()
            self.schemas[-1].apply_extensions()
            return
    def get(self, typename):
        for schema in self.schemas:
            if typename in schema:
                return schema.get(typename)


if __name__=="__main__":
    import sys
    if len(sys.argv)<2:
        exit(0)
    xsd_filename = sys.argv[1]
    parser = XSDParser(xsd_filename)
    
    print("Found {} schemas in {}".format(len(parser.schemas), xsd_filename))
    for schema in parser.schemas:
        print("Elements     : {}".format(len(schema.items)))
        print("SimpleTypes  : {}".format(len(schema.simple_types)))
        print("ComplexTypes : {}".format(len(schema.complex_types)))
        print("Groups       : {}".format(len(schema.groups)))
    if len(sys.argv)>2:
        for tn in sys.argv[2:]:
            print(parser.get(tn))
