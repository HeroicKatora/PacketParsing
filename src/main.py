'''
Created on 13.03.2016

@author: andreas
'''
from xmlparsing import XMLRegistry


if __name__ == '__main__':
    xmlReg = XMLRegistry()
    xmlReg.addSchemaFile('./schemes/PacketSchema.xsd')
    print(xmlReg.parser._namespace_map)
