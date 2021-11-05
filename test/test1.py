import tkinter as tk
from tkinter import ttk

from enum import Enum
from lxml import etree

class xsdtags(Enum):
    SCHEMA="schema"
    ELEMENT="element"
    SIMPLE_TYPE="simpleType"
    COMPLEX_TYPE="complexType"
    ENUMERATION="enumeration"
    SEQUENCE="sequence"
    CHOICE="choice"

def find_type_definition(xsd, name):
    for el in xsd.iter("{*}complexType", "{*}simpleType"):
        if "name" in el.attrib:
            if el.attrib["name"]==name:
                return el
    return None

def describe_schema(xsd, element):
    # go through elements and choices and print their description
    for e in element:
        if isinstance(e, etree._Comment):
            continue
        elif e.tag.endswith("element"):
            describe_element(xsd, e)
        elif e.tag.endswith("choice"):
            describe_choice(xsd, e)
        else:
            pass
def describe_element(xsd, element, lvl=0):
    print("{}- {}".format(lvl*" ",element.attrib["name"]))
    # get the type definition 
    _type = element.attrib["type"]
    if ":" in _type:
        _type = _type.split(":")[-1]
    d = find_type_definition(xsd, _type)
    # iterate over elements of the definition and describe them
    for el in d:
        if el.tag.endswith("sequence"):
            print("{}- seq :".format((lvl+1)*" "))
            for item in el:
                if item.tag.endswith("element"):
                    describe_element(xsd, item, lvl+2)
                if item.tag.endswith("choice"):
                    print("{}- choice :".format((lvl+2)*" "), item.attrib)
                    for c in item:
                        if c.tag.endswith("element"):
                            describe_element(xsd, c, lvl+3)


def describe_choice(xsd, element):
    print("describe choice {}".format(element.tag))
"""
A single XSD file can contain multiple schema definitions. Find each one and list the complexTypes that
are defined therein.
"""
if __name__=="__main__":
    xsd_filename = "spase-2.3.1.xsd"
    # load the tree
    xsd_tree = etree.parse(xsd_filename)
    
    # list all schemas in the XSD file
    for schema_el in xsd_tree.iter(tag="{*}schema"):
        print("Schema name : ",schema_el)
        describe_schema(xsd_tree, schema_el)

    exit()
