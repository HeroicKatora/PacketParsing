from src.gpp import XMLRegistry, build_parser
from src.gpp.xmlparsing import SchemeLibrary
import unittest


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.registry = XMLRegistry()

    def test_build(self):
        self.registry.add_library('Standard')
        parser = build_parser(self.registry)
        self.assertTrue(('http://github.com/HeroicKatora/PacketParsing/Standard', 'StandardDocument') in parser.documents_map.keys())
