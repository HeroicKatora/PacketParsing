'''
Created on 14.03.2016

@author: andreas
'''
from ..builtin.builtin import deviate_builtin, qualifier_gpp,\
    parsehandle, parse_dependency
from ..xmlparsing.builder import parse_object
from .types import Enumeration, EnumValue
from .types import IntegralDisplay, IntegralType
from .types import Field, Sequence


namespace_std = "http://github.com/HeroicKatora/PacketParsing/Standard"
qualifier_std = '{'+namespace_std+'}'


def parsed(xml, document_builder):
    parser = parsehandle(xml, document_builder)
    encoded = xml.get('value')
    return parser.parse(encoded)


def enumeration(xml, document_builder):
    fallback = xml.find(qualifier_std+'enum_fallback')
    values = [deviate_builtin(xml_val, document_builder, parse_object)
            for xml_val in xml.findall(qualifier_std+'enumvalue')]
    return Enumeration(values, fallback)

def enumvalue(xml, document_builder):
    parsed = parse_object(xml.find(qualifier_std+'parsed'), document_builder)
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
    submodules = list(parse_object(mod, document_builder) for mod in xml.findall(qualifier_gpp+'submodule'))
    return Sequence(submodules)


def field(xml, document_builder):
    typ = xml.get('type')
    typ = parse_dependency(('type', typ), document_builder)
    displayname = xml.get('displayname')
    values = list(parse_object(val, document_builder) for val in xml.findall(qualifier_gpp+'parsed')) or None
    return Field(typ, displayname, values)
