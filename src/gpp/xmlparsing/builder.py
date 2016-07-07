import importlib

from collections import namedtuple
from itertools import dropwhile
from re import match
from lxml import etree

from . import  XMLRegistry
from .interfaces import PacketDocument, PacketParser

from .builtin import namespace_gpp
from .standard import namespace_std


gpp_object_types = ('type', 'io', 'reader', 'writer', 'display', 'parser', 'printer')


TagInfo = namedtuple('TagInfo', 'namespace basetag')
def tag_split(t):
    match_t = match('{(.*)}(.*)', t.tag)
    if match_t is None:
        return None
    groups = match_t.groups()
    if len(groups) < 1:
        return None
    return TagInfo._make(groups)


Builder = namedtuple('Builder', 'xml_reg tbd progress done')
def build_parser(xml_registry: XMLRegistry):
    full_schema = etree.XMLSchema(xml_registry.schema_tree)
    parser = etree.XMLParser(schema=full_schema, attribute_defaults=True, remove_blank_text=True, resolve_entities=True)
    tbd, progress, done = dict(), dict(), dict()
    builder = Builder(xml_registry, tbd, progress, done)
    for xml_file, library in xml_registry.validation_list:
        parsed_tree = etree.parse(xml_file, parser)
        document_name = parsed_tree.getroot().get('document_name')
        tbd[(library, document_name)] = parsed_tree
    while tbd:
        (lib, doc), tree = tbd.popitem()
        parse_document(builder, lib, doc, tree)
    packet_parser = PacketParser(xml_registry, done)
    return packet_parser


DocumentBuilder = namedtuple('DocumentBuilder', 'builder lib doc tree document parse_stack')
def parse_document(builder, lib, doc, tree):
    doc_key = (lib, doc)
    xml_reg, progress, tbd, done = builder.xml_reg, builder.progress, builder.tbd, builder.done

    tree = tbd.pop(doc_key, None) or tree
    progress[doc_key] = tree
    root = tree.getroot()
    namespaces = {l: k for k, l in root.nsmap.items() if k != 'xsi'}
    for name in set(namespaces.keys()) - set(xml_reg.namespace_implementors.keys()):
        print('Unknown namespace %s defined in %s, %s' % (name, lib, doc))

    namespace_implementors = {l: xml_reg.namespace_implementors.get(l, None)
            for l in namespaces.keys()}
    document = PacketDocument(root, namespace_implementors)
    document_builder = DocumentBuilder(builder, lib, doc, tree, document, [])

    doc_objects = root.iterchildren()
    parse_document_objects(doc_objects, document_builder)
    done[doc_key] = document
    return document


def resolve_load_document(builder, lib, doc):
    key = (lib, doc)
    done, progress, tbd = builder.done, builder.progress, builder.tbd
    if key in done:
        return done[key]
    if key in progress:
        raise CircularIncludeError()
    try:
        tree = tbd.pop(key)
        return parse_document(builder, lib, doc, tree)
    except KeyError:
        raise MissingFileError('%s not found in %s, have you imported the correct libraries?' % (doc, lib))


def parse_document_objects(doc_iter, document_builder):
    document = document_builder.document
    by_name = document.source_map = {(tag_split(do).basetag, do.get('name')): do for do in doc_iter}
    done = document.all_objects
    for key, item in by_name.items():
        if key not in done:
            parse_object(item, document_builder)
    for (typ, name), obj in done.items():
        getattr(document, typ)[name] = obj


def parse_object(item, document_builder):
    if item in document_builder.parse_stack:
        raise CircularReferenceError()
    document_builder.parse_stack.append(item)

    document = document_builder.document
    nodes = document.source_map
    done = document.all_objects
    #parse all dependencies
    dependencies = list()
    for typ in gpp_object_types:
        xpath = './/{' + namespace_gpp + '}' + typ + '_ref'
        for dep in item.findall(xpath):
            key = (typ, dep.get('ref_name'))
            dependencies.append(key)
    for key in dependencies:
        typ, name = key
        if key in done:
            continue
        dep = nodes[key]
        parse_object(dep, document_builder)

    #delegate to implementor
    item_tag = tag_split(item)
    item_ns = item_tag.namespace
    item_basetag = item_tag.basetag
    item_key = item_basetag, item.get('name')

    parsed = parse_resolve_object(item, document_builder)
    done[item_key] = parsed

    document_builder.parse_stack.pop()
    return parsed


reserved_keywords = ('False','def','if','raise','None','del','import','return','True','elif','in','try','and',
    'else','is','while','as','except','lambda','with','assert','finally','nonlocal','yield','break','for','not',
    'class','from','or','continue','global','pass')
def parse_resolve_object(item, document_builder):
    item_tag = tag_split(item)
    item_ns = item_tag.namespace
    item_basetag = item_tag.basetag

    if item_basetag in reserved_keywords:
        item_basetag += '_'
    module = document_builder.document.namespace_implementors[item_ns]
    return getattr(module, item_basetag)(item, document_builder)


class CircularIncludeError(RuntimeError):
    '''Thrown when documents include objects of each other
    '''
    pass
class MissingFileError(RuntimeError):
    '''Thrown when an included file does not exist
    '''
    pass
class CircularReferenceError(RuntimeError):
    '''Thrown when packet parsing objects require one another
    '''
    pass
