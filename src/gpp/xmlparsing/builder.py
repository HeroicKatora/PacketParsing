import importlib

from collections import namedtuple
from itertools import tee
from re import match
import re as regex
from lxml import etree

from .xmlregistry import XMLRegistry, GppResolver, FileSource, StringSource
from .interfaces import PacketDocument, PacketParser


gpp_object_types = ('type', 'io', 'reader', 'writer', 'display', 'parser',
        'printer', 'global_module')


TagInfo = namedtuple('TagInfo', 'namespace basetag')
def tag_split(t):
    prefix = t.prefix
    namesp = t.nsmap[prefix]
    unqualified = t.tag
    if namesp is None:
        return TagInfo(namesp, unqualified)
    assert(unqualified.startswith('{'+namesp+'}'))
    unqualified = unqualified[2+len(namesp):]
    return TagInfo(namesp, unqualified)


def gpp_key(xml):
    basetag = tag_split(xml).basetag
    return (basetag, xml.get('name'))


def parsed_xml_source(xml_source, xml_registry):
    parser = xml_registry.parser
    if isinstance(xml_source, FileSource):
        return etree.parse(xml_source.file, parser)
    elif isinstance(xml_source, StringSource):
        return etree.fromstring(xml_source.content, parser)
    elif isinstance(xml_source, str):
        return etree.fromstring(xml_source)
    raise IOError('Unkown source type of instance file')

Builder = namedtuple('Builder', 'xml_reg tbd progress done')
def build_parser(xml_registry: XMLRegistry):
    full_schema = etree.XMLSchema(xml_registry.schema_tree)
    parser = etree.XMLParser(schema=full_schema, attribute_defaults=True, remove_blank_text=True, resolve_entities=True)
    parser.resolvers.add(xml_registry.resolver)

    tbd, progress, done = dict(), dict(), dict()
    builder = Builder(xml_registry, tbd, progress, done)
    for xml_source, library in xml_registry.validation_list:
        parsed_tree = parsed_xml_source(xml_source, xml_registry)
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
    doc_iter, to_map = tee(doc_iter)
    by_name = document.source_map = {(tag_split(do).basetag, do.get('name')): do for do in to_map}
    done = document.all_objects
    for item in doc_iter:
        if item not in done.values():
            parse_object(item, document_builder)
    for (typ, name), obj in done.items():
        if typ in gpp_object_types:
            getattr(document, typ)[name] = obj


def parse_object(item, document_builder):
    if item in document_builder.parse_stack:
        raise CircularReferenceError()
    document_builder.parse_stack.append(item)

    document = document_builder.document
    nodes = document.source_map
    done = document.all_objects

    #delegate to implementor
    item_tag = tag_split(item)
    item_ns = item_tag.namespace
    item_basetag = item_tag.basetag
    item_key = item_basetag, item.get('name')
    try:
        parsed = parse_resolve_object(item, document_builder)
    except Exception as ex:
        raise Exception('in {}, line {}'.format(item_tag, item.sourceline)) from ex
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
