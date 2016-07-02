"""
Created on 13.03.2016

@author: andreas
"""

from enum import Enum
from builtins import str, KeyError
from lxml import etree

from . import builtin


class XMLRegistry:
    def __init__(self):
        self.XS = "{http://www.w3.org/2001/XMLSchema}"
        self.XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
        with open('./template.xml') as template:
            self.schema_tree = etree.parse(template)
        self.validation_list = list()
        self.namespace_implementors = dict()

        self.add_schema_file('schemes/PacketSchema.xsd', builtin)
        self.add_library(SchemeLibrary.Builtin)

    def add_schema_file(self, source_uri, implementing_module):
        parsed_schema = etree.parse(source_uri)
        namespace = parsed_schema.getroot().get('targetNamespace')
        import_xs = etree.Element(self.XS+'import')
        import_xs.attrib['namespace'] = namespace
        import_xs.attrib['schemaLocation'] = source_uri
        self.namespace_implementors[namespace] = implementing_module
        self.schema_tree.getroot().append(import_xs)

    def add_instance_file(self, source_uri, lib_name=None):
        self.validation_list.append((source_uri, lib_name))

    def add_library(self, library):
        """
        Use a string or a PacketLibrary object to add to the XMLRegistry
        :param library: If a string, tries to resolves the corresponding SchemeLibrary Enum.
            Else tries to add the object as a PacketLibrary
        """
        try:
            if library.__class__ is str:
                lib_collect = SchemeLibrary(library)
                return self.add_library(lib_collect)
            elif library.__class__ is SchemeLibrary:
                library = library.value
                for file, module in library.schemes():
                    self.add_schema_file(file, module)
                for file in library.xml():
                    self.add_instance_file(file, library.identifier())
        except Exception as e:
            raise KeyError('Can\'t construct a library from the argument')


class SchemeLibrary(Enum):
    Builtin = builtin.library
