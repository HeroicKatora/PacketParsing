from . import builtin as impl
from ..xmlparsing.interfaces import SimpleLibrary
from ..xmlparsing.xmlregistry import FileSource, BuiltinName


library = SimpleLibrary(impl.namespace_gpp,
        [(FileSource('schemes/PacketSchema.xsd'), impl)],
        [])
