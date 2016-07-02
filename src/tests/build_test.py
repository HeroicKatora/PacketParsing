from src.gpp import XMLRegistry, build_parser
import unittest


class BuildTest(unittest.TestCase):
    def setUp(self):
        self.registry = XMLRegistry()

    def test_build(self):
        parser = build_parser(self.registry)
        print(parser.documents_map)
