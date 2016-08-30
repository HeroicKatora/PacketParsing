'''
Created on 05.06.2016

Implements all types and objects delcared in PacketSchema.xsd.
That is everything but the main document root tree, including imports and includes.

@author: andreas
'''

# Forward declare the library to avoid import problems
from . import builtin as impl
from .interfaces import SimpleLibrary
from .builder import parse_object, tag_split
from .xmlregistry import FileSource
from ..exec import types


namespace_gpp = "http://github.com/HeroicKatora/PacketParsing"
library = SimpleLibrary(namespace_gpp,
        [(FileSource('schemes/PacketSchema.xsd'), impl)],
        [])


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
    name = xml.get('ref_name')
    key = (typ, name)
    document = document_builder.document
    obj = document.all_objects.get(key, None)
    if obj is not None:
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
    return deviate_builtin(xml, document_builder, type_impl)

def type_impl(xml, document_builder):
    name = xml.get('name')
    children = xml.getchildren()
    first_name = tag_split(children[0]).basetag
    if first_name == 'typehandle':
        assert(len(children) == 1)
        typ = parse_object(children[0], document_builder)
        return types.Type(name, typ, typ, typ, typ)
    reader, writer = io_group(xml, document_builder)
    parser, printer = display_group(xml, document_builder)
    return types.Type(name, reader, writer, parser, printer)


def io_operator(xml, document_builder):
    return deviate_builtin(xml, document_builder, io_impl)

def io_impl(xml, document_builder):
    name = xml.get('name')
    reader, writer = io_group(xml, document_builder)
    return types.IO(name, reader, writer)


def display(xml, document_builder):
    return deviate_builtin(xml, document_builder, display_impl)

def display_impl(xml, document_builder):
    name = xml.get('name')
    parser, printer = display_group(xml, document_builder)
    return types.Display(name, parser, printer)


def parser(xml, document_builder):
    return deviate_builtin(xml, document_builder, parser_impl)

def parser_impl(xml, document_builder):
    name = xml.get('name')
    parsehandle = xml.find('parsehandle')
    return types.Parser(name, parsehandle)


def printer(xml, document_builder):
    return deviate_builtin(xml, document_builder, printer_impl)

def printer_impl(xml, document_builder):
    name = xml.get('name')
    printhandle = xml.find('printhandle')
    return types.Printer(name, printhandle)


def reader(xml, document_builder):
    return deviate_builtin(xml, document_builder, reader_impl)

def reader_impl(xml, document_builder):
    name = xml.get('name')
    readhandle = xml.find('readhandle')
    return types.Reader(name, readhandle)


def writer(xml, document_builder):
    return deviate_builtin(xml, document_builder, writer_impl)

def writer_impl(xml, document_builder):
    name = xml.get('name')
    writehandle = xml.find('writehandle')
    return types.Printer(name, writehandle)


# Utility methods for the construction above


def deviate_builtin(xml, document_builder, elsecall):
    '''Checks if the only child is of type gpp:builtin. If it is, returns the
    referenced include and if it is not, calls elsecall with its other arguments.
    '''
    children = xml.getchildren()
    first_tag = tag_split(children[0])
    if first_tag.basetag == 'builtin' and first_tag.namespace == namespace_gpp:
        return builtin(children[0], document_builder)
    return elsecall(xml, document_builder)


def io_group(xml, document_builder):
    iohandle_obj = xml.find('iohandle')
    if iohandle_obj:
        ioop = parse_object(iohandle_obj, document_builder)
        return ioop, ioop
    readhandle_obj = xml.find('readhandle')
    writehandle_obj = xml.find('writehandle')
    reader = parse_object(readhandle_obj, document_builder)
    writer = parse_object(writehandle_obj, document_builder)
    return reader, writer


def display_group(xml, document_builder):
    displayhandle_obj = xml.find('displayhandle')
    if displayhandle_obj:
        display = parse_object(displayhandle_obj, document_builder)
        return display, display
    parsehandle_obj = xml.find('parsehandle')
    printhandle_obj = xml.find('printhandle')
    parser = parse_object(parsehandle_obj, document_builder)
    printer = parse_object(printhandle_obj, document_builder)
    return parser, printer



# Handler construction


def handle_build(xml, document_builder):
    return deviate_builtin(xml, document_builder, handle_impl)

def handle_impl(xml, document_builder):
    return parse_object(xml.getchildren()[0], document_builder)


# All handles are built exactly the same way


typehandle = handle_build
iohandle = handle_build
displayhandle = handle_build
readhandle = handle_build
writehandle = handle_build
printhandle = handle_build
parsehandle = handle_build

###############################################################################
#                                                                             #
#   Module stuff                                                              #
#                                                                             #
###############################################################################


def global_module(xml, document_builder):
    return deviate_bulttin(xml, document_builder, global_module_impl)

def global_module_impl(xml, document_builder):
    xml_module = xml.getchildren()[0]
    name = xml.get('name')
    module = parse_object(xml_module, document_builder)
    module_map = document_builder.document.global_module
    return module


def module_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'global_module')


def submodule(xml, document_builder):
    pass
