import importlib
from . import standard as standard_package
from lxml import etree
from .interfaces import SimpleLibrary, PacketDocument, PacketParser
from collections import namedtuple
from itertools import dropwhile
from re import match


namespace_gpp = "http://github.com/HeroicKatora/PacketParsing"
namespace_std = "http://github.com/HeroicKatora/PacketParsing/Standard"


library = SimpleLibrary(namespace_std,
                [('schemes/StandardTypes.xsd', standard_package)],
                ['xml/StandardDocument.xml'])
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


def build_parser(xml_registry):
    full_schema = etree.XMLSchema(xml_registry.schema_tree)
    parser = etree.XMLParser(schema=full_schema, attribute_defaults=True, remove_blank_text=True, resolve_entities=True)
    tbd, progress, done = dict(), dict(), dict()
    for xml_file, library in xml_registry.validation_list:
        parsed_tree = etree.parse(xml_file, parser)
        document_name = parsed_tree.getroot().get('document_name')
        tbd[(library, document_name)] = parsed_tree
    while tbd:
        (lib, doc), tree = tbd.popitem()
        parse_document(xml_registry, lib, doc, tree, tbd, progress, done)

    packet_parser = PacketParser(xml_registry, done)
    return packet_parser

def parse_document(xml_reg, lib, doc, tree, tbd, progress, done):
    doc_key = (lib, doc)
    progress[doc_key] = tree
    root = tree.getroot()
    namespaces = {l: k for k, l in root.nsmap.items() if k != 'xsi'}
    for name in set(namespaces.keys()) - set(xml_reg.namespace_implementors.keys()):
        print('Unknown namespace %s defined in %s, %s' % (name, lib, doc))

    namespace_implementors = {l: xml_reg.namespace_implementors.get(l, None)
            for l in namespaces.keys()}
    document = PacketDocument(root, namespace_implementors)

    for imp in root.findall('{%s}import' % namespace_gpp):
        module_name = imp.get('module')
        module_inst = importlib.import_module(module_name)
        for instantiator_import in imp.findall('{%s}instantiator_import' % namespace_gpp):
            name = instantiator_import.get('name')
            instance_name = instantiator_import.get('instance_name')
            obj = getattr(module_inst, 'instance_name')
            document.imported_objects[name] = obj

    for include in root.findall('{%s}include' % namespace_gpp):
        incl_lib = include.get('library_name')
        incl_doc_name = include.get('document_name')
        incl_document = resolve_load_document(xml_reg, inc_lib, incl_doc_name, tbd, progress, done)
        for def_include in include.getchildren():
            incl_type = tag_name(def_include)
            incl_name = def_include.get('name')
            incl_instance_name = def_include.get('instance_name')
            incl_obj = getattr(incl_document, incl_type)[incl_instance_name]
            getattr(document, incl_type)[incl_name] = incl_obj
    children = root.iterchildren()
    doc_objects = dropwhile(lambda t: tag_split(t).basetag in ('import', 'include'), children)

    parse_document_objects(doc_objects, document)
    done[doc_key] = document
    return document


def parse_document_objects(doc_iter, document):
    by_name = {(tag_split(do).basetag, do.get('name')): do for do in doc_iter}
    done = document.all_objects
    while by_name:
        (typ, name), item = by_name.popitem()
        parse_object(item, (item,), by_name, done, document)
    for (typ, name), obj in done.items():
        getattr(document, typ)[name] = obj


def parse_object(item, stack, nodes, done, document):
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
        if dep in stack:
            raise CircularReferenceError()
        parse_object(dep, stack+(dep,), nodes, done, document)

    #delegate to implementor
    item_tag = tag_split(item)
    item_ns = item_tag.namespace
    item_basetag = item_tag.basetag
    item_key = item_basetag, item.get('name')

    parsed = parse_resolve_object(item, document)
    done[item_key] = parsed
    return parsed


def parse_resolve_object(item, document):
    item_tag = tag_split(item)
    item_ns = item_tag.namespace
    item_basetag = item_tag.basetag

    module = document.namespace_implementors[item_ns]
    return getattr(module, item_basetag)(item, document)


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


def resolve_load_document(xml_reg, lib, doc, tbd, progress, done):
    key = (lib, doc)
    if key in done:
        return done[key]
    if key in progress:
        raise CircularIncludeError()
    try:
        tree = tbd.pop(key)
        return parse_document(xml_reg, lib, doc, tree, tbd, progress, done)
    except KeyError:
        raise MissingFileError('%s not found in %s, have you imported the correct libraries?' % (doc, lib))


def global_module():
    pass


def type(xml, document):
    #print('type', xml.get('name'))
    return xml.get('name')
