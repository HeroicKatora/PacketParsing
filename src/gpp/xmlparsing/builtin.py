'''
Created on 05.06.2016

@author: andreas
'''

from .interfaces import SimpleLibrary
from . import builtin as impl
namespace_gpp = "http://github.com/HeroicKatora/PacketParsing"
library = SimpleLibrary(namespace_gpp,
        [('schemes/PacketSchema.xsd', impl)],
        [])


from .builder import parse_object, tag_split
from ..exec import types


def builtin(xml, document_builder):
    document = document_builder.document
    name = xml.get('implementor')
    return document.imported_objects[name]


def import_(imp, document_builder):
    document = document_builder.document
    module_name = imp.get('module')
    module_inst = importlib.import_module(module_name)
    for instantiator_import in imp.findall('{%s}instantiator_import' % namespace_gpp):
        name = instantiator_import.get('name')
        instance_name = instantiator_import.get('instance_name')
        obj = getattr(module_inst, 'instance_name')
        document.imported_objects[name] = obj


def include(inc, document_builder):
    document = document_builder.document
    incl_lib = include.get('library_name')
    incl_doc_name = include.get('document_name')
    incl_document = resolve_load_document(builder, inc_lib, incl_doc_name)
    for def_include in include.getchildren():
        incl_type = tag_name(def_include)
        incl_name = def_include.get('name')
        incl_instance_name = def_include.get('instance_name')
        incl_obj = getattr(incl_document, incl_type)[incl_instance_name]
        getattr(document, incl_type)[incl_name] = incl_obj


def type_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'type')
def io_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'io')
def reader_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'reader')
def writer_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'writer')
def display_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'display')
def printer_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'printer')
def parser_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'parser')


def object_dependency(xml, document_builder, typ):
    name = xml.get('name')
    key = (typ, name)
    document = document_builder.document
    obj = document.all_objects.get(key, None)
    if obj:
        return obj
    obj = document.source_map[key]
    obj = parse_object(obj, document_builder)
    return obj


###############################################################################
#                                                                             #
#   Major type construction                                                   #
#                                                                             #
###############################################################################


def type(xml, document_builder):
    name = xml.get('name')
    children = xml.getchildren()
    first_name = tag_split(children[0]).basetag
    if first_name == 'typehandle' or first_name == 'builtin':
        assert(len(children) == 1)
        typ = parse_object(children[0], document_builder)
        return types.Type(name, typ, typ, typ, typ)
    reader, writer = io_group(xml, document_builder)
    parser, printer = display_group(xml, document_builder)
    return types.Type(name, reader, writer, parser, printer)


def io_operator(xml, document_builder):
    #TODO implement
    pass

def display(xml, document_builder):
    #TODO implement
    pass

def parser(xml, document_builder):
    #TODO implement
    pass

def printer(xml, document_builder):
    #TODO implement
    pass

def reader(xml, document_builder):
    #TODO implement
    pass

def writer(xml, document_builder):
    #TODO implement
    pass


def io_group(xml, document_builder):
    iohandle = xml.find('iohandle')
    if iohandle:
        ioop = parse_object(iohandle, document_builder)
        return ioop, ioop
    readhandle = xml.find('readhandle')
    writehandle = xml.find('writehandle')
    reader = parse_object(readhandle, document_builder)
    writer = parse_object(writehandle, document_builder)
    return reader, writer


def display_group(xml, document_builder):
    displayhandle = xml.find('displayhandle')
    if displayhandle:
        display = parse_object(displayhandle, document_builder)
        return display, display
    parsehandle = xml.find('parsehandle')
    printhandle = xml.find('printhandle')
    parser = parse_object(parsehandle, document_builder)
    printer = parse_object(printhandle, document_builder)
    return parser, printer



# Type handler construction


def typehandle(xml, document_builder):
    #TODO implement
    pass

def iohandle(xml, document_builder):
    #TODO implement
    pass

def displayhandle(xml, document_builder):
    #TODO implement
    pass

def readhandle(xml, document_builder):
    #TODO implement
    pass
    #TODO implement

def writehandle(xml, document_builder):
    pass

def printhandle(xml, document_builder):
    #TODO implement
    pass

def parsehandle(xml, document_builder):
    #TODO implement
    pass


###############################################################################
#                                                                             #
#   Module stuff                                                              #
#                                                                             #
###############################################################################


def global_module(xml, document_builder):
    #TODO implement
    pass

def module_ref(xml, document_builder):
    #TODO implement
    pass
