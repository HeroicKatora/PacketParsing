from gpp import XMLRegistry, build_parser
from gpp.xmlparsing import SchemeLibrary, FileSource, local_file
from gpp.standard import StandardName
import unittest


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.registry = XMLRegistry()
        self.registry.add_library(StandardName)
        self.parser = build_parser(self.registry)

    def test_exists(self):
        self.assertTrue((StandardName, 'StandardDocument') in self.parser.documents_map.keys())

    def test_parsed(self):
        self.registry.add_instance(local_file(__file__, '../xml/IPv4Types.xml'))
        build_parser(self.registry)
