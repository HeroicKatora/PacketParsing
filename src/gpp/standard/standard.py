'''
Created on 14.03.2016

@author: andreas
'''
from ..builtin.builtin import deviate_builtin
from ..xmlparsing.builder import parse_object
from .types import Enumeration, EnumValue
from .types import DisplayIntegral, TypeIntegral


namespace_std = "http://github.com/HeroicKatora/PacketParsing/Standard"


def enumeration(xml, document_builder):
    fallback = xml.find('enum_fallback')
    values = [deviate_builtin(xml_val, document_builder, enumvalue)
            for xml_val in xml.findall('enumvalue')]
    return Enumeration(values, fallback)

def enumvalue(xml, document_builder):
    parsed = parse_object(xml.find('parsed'))
    mnemonic = xml.get('mnemonic')
    return EnumValue(mnemonic, parsed)


def display_integral(xml, document_builder):
    pass


def integral(xml, document_builder):
    pass


def sequence(xml, document_builder):
    pass


def join_module(xmlTree):
    pass


def match_module(xmlTree):
    pass
