from . import standard as impl
from ..xmlparsing.interfaces import SimpleLibrary
from ..xmlparsing.xmlregistry import FileSource


StandardName = 'gpp.standard'
library = SimpleLibrary(StandardName,
                [(FileSource('schemes/StandardTypes.xsd'), impl)],
                [FileSource('xml/StandardDocument.xml')])
