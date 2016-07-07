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


from .builder import parse_object


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
def parser_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'parser')
def printer_ref(xml, document_builder):
    return object_dependency(xml, document_builder, 'printer')


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


def type(xml, document):
    print('type', xml.get('name'))
    return xml.get('name')
