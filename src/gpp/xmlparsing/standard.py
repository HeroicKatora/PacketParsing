'''
Created on 14.03.2016

@author: andreas
'''
from .interfaces import SimpleLibrary
from . import standard as impl
namespace_std = "http://github.com/HeroicKatora/PacketParsing/Standard"
library = SimpleLibrary(namespace_std,
                [('schemes/StandardTypes.xsd', __package__)],
                ['xml/StandardDocument.xml'])


def enumeration(xmlTree):
    pass


def display_integral(xmlTree):
    pass


def integral(xmlTree):
    pass


def instance_handle(xmlTree):
    pass


def join_module(xmlTree):
    pass


def match_module(xmlTree):
    pass


def imported(xml_tree, document_builder):
    pass
