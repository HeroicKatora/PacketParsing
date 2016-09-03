from src.gpp import XMLRegistry, build_parser
from src.gpp.xmlparsing import SchemeLibrary
import unittest


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.registry = XMLRegistry()
        self.registry.add_library('Standard')
        self.parser = build_parser(self.registry)

    def test_exists(self):
        self.assertTrue(('http://github.com/HeroicKatora/PacketParsing/Standard', 'StandardDocument') in self.parser.documents_map.keys())

    def test_parsed(self):
        self.assertTrue(True)
