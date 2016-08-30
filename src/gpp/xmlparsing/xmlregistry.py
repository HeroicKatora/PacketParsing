from builtins import str, KeyError
from collections import namedtuple
from lxml import etree

from .interfaces import PacketLibrary

gppresolverscheme = 'gppbuiltin'
class GppResolver(etree.Resolver):
    def __init__(self):
        super().__init__()
        self.schemes = dict()

    def add_schema_string(self, schemastr, namespace):
        self.schemes[namespace] = schemastr

    def make_identifier(self, namespace):
        return gppresolverscheme+':'+namespace

    def resolve(self, url, id, context):
        if not url.count(':'):
            return None
        scheme, namespace = url.split(':', 1)
        if scheme != gppresolverscheme:
            return None
        return self.schemes[namespace] and self.resolve_string(self.schemes[namespace], context)


FileSource = namedtuple('FileSource', 'file')
StringSource = namedtuple('StringSource', 'content')
class XMLRegistry:
    def __init__(self):
        self.XS = "{http://www.w3.org/2001/XMLSchema}"
        self.XSI = "{http://www.w3.org/2001/XMLSchema-instance}"
        self.validation_list = list()
        self.namespace_implementors = dict()
        self.resolver = GppResolver()
        self.parser = etree.XMLParser()
        self.parser.resolvers.add(self.resolver)
        with open('./template.xml') as template:
            self.schema_tree = etree.parse(template, self.parser)

        self.add_library(SchemeLibrary[BuiltinName])

    def add_schema(self, source, implementing_module):
        if isinstance(source, FileSource):
            return self.add_schema_file(source.file, implementing_module)
        elif isinstance(source, StringSource):
            return self.add_schema_string(source.content, implementing_module)
        elif isinstance(source, str):
            return self.add_schema_string(source, implementing_module)
        raise IOError('Unknown source type of schema file')

    def add_schema_string(self, source_string, implementing_module):
        parsed_schema = etree.fromstring(source_string, self.parser)
        namespace = parsed_schema.getroot().get('targetNamespace')
        import_xs = etree.Element(self.XS+'import')
        import_xs.attrib['namespace'] = namespace
        import_xs.attrib['schemaLocation'] = self.resolver.make_identifier(namespace)
        self.resolver.add_schema_string(source_string, namespace)
        self.namespace_implementors[namespace] = implementing_module
        self.schema_tree.getroot().append(import_xs)

    def add_schema_file(self, source_uri, implementing_module):
        parsed_schema = etree.parse(source_uri, self.parser)
        namespace = parsed_schema.getroot().get('targetNamespace')
        import_xs = etree.Element(self.XS+'import')
        import_xs.attrib['namespace'] = namespace
        import_xs.attrib['schemaLocation'] = self.resolver.make_identifier(namespace)
        self.resolver.add_schema_string(etree.tostring(parsed_schema.getroot()), namespace)
        self.namespace_implementors[namespace] = implementing_module
        self.schema_tree.getroot().append(import_xs)

    def add_instance(self, source, lib_name=None):
        if source.__class__ not in [FileSource, StringSource, str]:
            raise IOError('Unkown source type of instance file')
        self.validation_list.append((source, lib_name))

    def add_library(self, library):
        """
        Use a string or a PacketLibrary object to add to the XMLRegistry
        :param library: If a string, tries to resolves the corresponding SchemeLibrary Enum.
            Else tries to add the object as a PacketLibrary
        """
        if isinstance(library, str):
            lib_collect = SchemeLibrary[library.lower()]
            return self._add_library(lib_collect)
        return self._add_library(library)

    def _add_library(self, library):
        for file, module in library.schemes():
            self.add_schema(file, module)
        for file in library.xml():
            self.add_instance(file, library.identifier())

SchemeLibrary = dict()
BuiltinName = 'builtin'
def register_library(name: str, library: PacketLibrary):
    if not isinstance(name, str) or not isinstance(library, PacketLibrary):
        raise KeyError('Not a valid pair to register as a library')
    if SchemeLibrary.get(name.lower(), None):
        raise KeyError('A library is already registered with that name')
    SchemeLibrary[name.lower()] = library
