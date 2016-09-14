from . import builtin as impl
from ..xmlparsing.interfaces import SimpleLibrary
from ..xmlparsing.xmlregistry import FileSource, BuiltinName, local_file


library = SimpleLibrary(BuiltinName,
        [(local_file(__file__, 'PacketSchema.xsd'), impl)],
        [])
