'''
Created on 13.03.2016

@author: andreas
'''
from gpp.xmlparsing import XMLRegistry


class PacketContent():
    '''A part of a packet with dynamic size or content
    '''
    def read(self, bitstream):
        pass

    def write(self, bitstream):
        pass


class PacketField(PacketContent):
    '''A field has additional printing and parsing capabilities
    '''
    def print(self, charstream):
        pass

    def parse(self, charstream):
        pass

    def get(self):
        pass


if __name__ == '__main__':
    xmlReg = XMLRegistry()
    xmlReg.addSchemaFile('./schemes/PacketSchema.xsd')
    print(xmlReg.parser._namespace_map)
