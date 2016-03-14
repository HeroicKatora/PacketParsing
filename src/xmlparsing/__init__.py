'''
Created on 13.03.2016

@author: andreas
'''

from enum import Enum
from builtins import str, KeyError
from xml.etree import ElementTree
from xmlparsing import builtin


class SchemeLibrary(Enum):
    Builtin = builtin.library


class PacketLibrary():
    '''Library documentation class
    '''
    def schemes(self):
        '''Returns a collection of schemes
        '''
        pass

    def xml(self):
        '''Returns a collection of xml files for the library
        '''
        pass


class XMLRegistry():
    def __init__(self):
        self.parser = ElementTree
        self.validationList = list()
        self.schemes = dict()
        self.addLibrary(SchemeLibrary.Builtin)

    def addSchemaFile(self, sourceURI):
        parsedSchema = self.parser.parse(sourceURI)
        nameSpace = parsedSchema.getroot().get('targetNamespace')
        self.schemes.put(nameSpace, parsedSchema)

    def addInstanceFile(self, source):
        parsedData = self.parser.parse(source)
        self.validationList.append(parsedData)
        return parsedData

    def buildParser(self):
        pass

    def addLibrary(self, library):
        if library.__class__ is str:
            libCollect = SchemeLibrary(library)
            for file in libCollect.schemes():
                self.addSchemaFile(file)
            for file in libCollect.xml():
                self.addInstanceFile(file)
            return
        elif library.__class__ is SchemeLibrary:
            for file in library.schemes():
                self.addSchemaFile(file)
            for file in library.xml():
                self.addInstanceFile(file)
            return
        raise KeyError('Can\'t construct a library from the argument')
