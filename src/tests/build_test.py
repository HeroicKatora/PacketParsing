from src.gpp import XMLRegistry, build_parser
from src.gpp.xmlparsing import SchemeLibrary
import unittest


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.registry = XMLRegistry()

    def test_build(self):
        self.registry.add_library(SchemeLibrary.Standard)
        parser = build_parser(self.registry)
        print(parser.documents_map)
