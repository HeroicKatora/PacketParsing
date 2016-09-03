"""
Created on 13.03.2016

@author: andreas
"""
from .xmlparsing import XMLRegistry, register_library
from .xmlparsing.builder import build_parser

from .builtin import library as BuiltinLibrary, BuiltinName
from .standard import library as StandardLibrary, StandardName
register_library(BuiltinName, BuiltinLibrary)
register_library(StandardName, StandardLibrary)


def version():
    return '0.0.1'
