'''
Created on 14.03.2016

@author: andreas
'''
from .interfaces import SimpleLibrary
from .xmlregistry import FileSource
from . import standard as impl
namespace_std = "http://github.com/HeroicKatora/PacketParsing/Standard"
StandardName = 'standard'
library = SimpleLibrary(namespace_std,
                [(FileSource('schemes/StandardTypes.xsd'), impl)],
                [FileSource('xml/StandardDocument.xml')])


def enumeration(xmlTree):
    pass


def display_integral(xmlTree):
    pass


def integral(xml, document_builder):
    pass


def instance_handle(xmlTree):
    pass


def join_module(xmlTree):
    pass


def match_module(xmlTree):
    pass


def imported(xml_tree, document_builder):
    pass
