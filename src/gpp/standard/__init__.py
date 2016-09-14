from . import standard as impl
from ..xmlparsing.interfaces import SimpleLibrary
from ..xmlparsing.xmlregistry import FileSource, local_file


StandardName = 'gpp.standard'
library = SimpleLibrary(StandardName,
                [(local_file(__file__, 'StandardTypes.xsd'), impl)],
                [local_file(__file__, 'StandardDocument.xml')])
