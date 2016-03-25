"""
Created on 13.03.2016

@author: andreas
"""

from abc import ABCMeta, abstractclassmethod
from enum import Enum
from builtins import str, KeyError
from lxml import etree
from . import builtin


class SchemeLibrary(Enum):
    Builtin = builtin.library


class PacketLibrary(metaclass=ABCMeta):
    """
    Library documentation class
    """
    @abstractclassmethod
    def schemes(self):
        """
        :return: a collection of (schema, module) pairs added by the library
        """
        pass

    @abstractclassmethod
    def xml(self):
        """
        :return: a collection of xml files contained in the library
        """
        pass


class XMLRegistry():
    def __init__(self):
        self.XS = "{http://www.w3.org/2001/XMLSchema}"
        with open('./template.xml') as template:
            self.tempTree = etree.parse(template)
        self.parser = etree.ElementTree
        self.validationList = list()
        self.schemes = dict()
        self.addLibrary(SchemeLibrary.Builtin)
        self.namepsace_implementors = dict()

    def add_schema_file(self, source_uri, implementing_module):
        parsed_schema = self.parser.parse(source_uri)
        xml_schema = etree.XMLSchema(parsed_schema)
        namespace = parsed_schema.getroot().get('targetNamespace')
        import_xs = etree.Element(self.XS+'import')
        import_xs.attrib['namespace'] = namespace
        import_xs.attrib['schemaLocation'] = source_uri
        self.namepsace_implementors[namespace] = implementing_module
        self.tempTree.getroot().append(import_xs)

    def add_instance_file(self, source):
        self.validationList.append(source)

    def build_parser(self):
        pass

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
            else:
                for file, module in library.schemes():
                    self.add_schema_file(file, module)
                for file in library.xml():
                    self.add_instance_file(file)
                return
        except Exception:
            raise KeyError('Can\'t construct a library from the argument')
