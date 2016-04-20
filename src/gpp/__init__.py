"""
Created on 13.03.2016

@author: andreas
"""
from abc import ABCMeta, abstractclassmethod
from lxml import etree
from os import listdir

from gpp.xmlparsing import XMLRegistry


class PacketContent(metaclass=ABCMeta):
    """
    A part of a packet with dynamic size or content
    """
    @abstractclassmethod
    def read(self, bitstream):
        pass

    @abstractclassmethod
    def write(self, bitstream):
        pass


class PacketField(PacketContent,metaclass=ABCMeta):
    """
    A field has additional printing and parsing capabilities
    """
    @abstractclassmethod
    def print(self, charstream):
        pass

    @abstractclassmethod
    def parse(self, charstream):
        pass

    @abstractclassmethod
    def get(self):
        pass


if __name__ == '__main__':
    XS = "{http://www.w3.org/2001/XMLSchema}"
    print('Testing XML validation')
    with open('./template.xml') as template:
        tempTree = etree.parse(template)
    for file in filter(lambda p: p.endswith('.xsd'), listdir('./schemes')):
        location = '/'.join(('.', 'schemes', file))
        with open(location) as xsdFile:
            xsdScheme = etree.parse(xsdFile)
            namespace = xsdScheme.getroot().attrib['targetNamespace']
            print(namespace, ' found at file ', location)
            importXs = etree.Element(XS+'import')
            importXs.attrib['namespace'] = namespace
            importXs.attrib['schemaLocation'] = location
            tempTree.getroot().append(importXs)
    print(etree.tostring(tempTree, pretty_print=True).decode('UTF-8'))
    templateSchema = etree.XMLSchema(tempTree)
    parser = etree.XMLParser(schema=templateSchema, attribute_defaults=True, remove_blank_text=True, resolve_entities=True)
    tree = etree.parse('./xml/StandardDocument.xml', parser)
    print(etree.tostring(tree.getroot(), pretty_print=True).decode('UTF-8'))
    print('Testing element int64')
    int64 = tree.find('{http://github.com/HeroicKatora/PacketParsing}type')
    if int64 is None:
        print('Something went wrong')
    else:
        print(etree.tostring(int64).decode('UTF-8'))
