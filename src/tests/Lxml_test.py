from lxml import etree
import unittest


class UtilMethodTest(unittest.TestCase):
    def setUp(self):
        with open('./gpp/xmlparsing/template.xml') as template:
            self.tree = etree.parse(template)

    def test_tag_name(self):
        from gpp.xmlparsing.builder import tag_split
        el = self.tree.getroot()
        self.assertEqual(tag_split(el).basetag, 'schema')

if __name__ == "__main__":
    unittest.main()
