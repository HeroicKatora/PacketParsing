from . import standard as impl
from ..xmlparsing.interfaces import SimpleLibrary
from ..xmlparsing.xmlregistry import FileSource


StandardName = 'standard'
library = SimpleLibrary(impl.namespace_std,
                [(FileSource('schemes/StandardTypes.xsd'), impl)],
                [FileSource('xml/StandardDocument.xml')])
