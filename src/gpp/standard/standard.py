'''
Created on 14.03.2016

@author: andreas
'''
from ..builtin.builtin import deviate_builtin
from ..xmlparsing.builder import parse_object
from .types import Enumeration, EnumValue
from .types import IntegralDisplay, IntegralType


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
    formatstring = xml.get('formatstring') or '{:d}'
    return IntegralDisplay(formatstring)


def integral(xml, document_builder):
    formatstring = xml.get('formatstring') or '{:d}'
    subtype = xml.get('subtype') or 'int'
    return IntegralType(subtype, formatstring)


def sequence(xml, document_builder):
    submodules = list(parse_object(mod) for mod in xml.findall('submodule'))
    return Sequence(modules)


def field(xml, document_builder):
    typ = xml.get('type')
    displayname = xml.get('displayname')
    values = list(parse_object(val) for val in xml.findall('parsed')) or None
    return Field(typ, displayname, values)
