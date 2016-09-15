from gpp import XMLRegistry, build_parser
from gpp.xmlparsing import SchemeLibrary, local_file
from gpp.builtin import BuiltinName
from gpp.standard import StandardName
from bitstring import BitStream
import unittest


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.registry = XMLRegistry()
        self.registry.add_library(StandardName)
        self.registry.add_instance(local_file(__file__, '../xml/IPv4Types.xml'))
        self.parser = build_parser(self.registry)

    def test_IP4_header(self):
        ipv4 = self.parser.documents_map[(None, 'IPv4Types')]
        header_length = ipv4.type['IP_HL']
        ipv4_header = ipv4.global_module['IPv4_header']
        bitstring_hl = BitStream(bin='01011111')
        bitstring_header = BitStream(hex='4800dead''beef1234''ff3fbbcc''deadbeef''feebdaed')
        self.assertEqual(header_length.parse('16'), 16)
        self.assertEqual(header_length.read(bitstring_hl), 5)
        header = ipv4_header.read(bitstring_header)
        self.assertEqual(header['version'], 4)
