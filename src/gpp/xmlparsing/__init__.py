"""
Created on 13.03.2016

@author: andreas
"""

from .builder import build_parser
from .xmlregistry import XMLRegistry, FileSource, StringSource, from_local_file
from .xmlregistry import SchemeLibrary, register_library, BuiltinName

from .builtin import library as BuiltinLibrary
from .standard import library as StandardLibrary, StandardName
register_library(BuiltinName, BuiltinLibrary)
register_library(StandardName, StandardLibrary)
