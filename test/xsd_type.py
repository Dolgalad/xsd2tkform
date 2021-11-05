"""Implementation of the base XSDType object inherited by XSDSimpleTypeFrame and XSDComplexTypeFrame

Notes concerning components of this package : 
    - take XSD schema as input and generate Tkinter forms satisfying the definition of type included
    therein
    - XSD form : in this module a Form object is an instance of a graphical interface component. 
    A Form is a collection of input fields organised in a way that allows the user the edit the contents
    of an XML document. The final document must satisfy the type definitions found in the schema.
      A Tkinter Form object is a frame that contains widgets allowing the user to input values according
    to the types defined in an XSD schema.
    - a single XSD schema includes the definition of multiple types, complex and simple. Each of these
    types has an associated Form object. XSD Forms are constructed by piecing together multiple Forms.
    - a Generator instance is used to instantiate Forms, for example we may want to do something like:
            >>> form_generator = Generator(xsd_file = "xsd_file.xsd")
            >>> form = form_generator.get_form(type = "Type1")
            >>> isinstance(form, tk.Frame)
            True

    - a parser is needed to extract type definitions from the XSD schema file. This module uses the lxml
    module for parsing XML documents. Usage example : 
            >>> xsd_filename = "myxsd.xsd"
            >>> parser = Parser(xsd_file = xsd_filename)
            >>> # simpleTypes, complexTypes, groups definitions are available through dictionaries
            >>> parser.simple_types
            ...
            >>> parser.complex_types
            ...
            >>> parser.groups
            ...
     
    - XSD Types come in a variety of formats : supported are simpleType, compleType, group. A type has
    a name, and a description of input types. 
    - SimpleType objects are standalone : they do not depend on any other types in the schema. They are
    the easiest to implement. They have a name, an input type (which can be an enumeration of values)
    - ComplexType objects are aggregates of SimpleType objects as well as other ComplexType objects.


"""

"""
Base class for all XSD types
"""
class XSDType:
    def __init__(self, name=None):
        self.name = name

class XSDSimpleType(XSDType):
    def __init__(self, name=None, input_type=None):
        XSDType.__init__(self, name)
        self.input_type = input_type

class XSDComplexType(XSDType):
    def __init__(self, name=None):
        XSDType.__init__(self, name)
