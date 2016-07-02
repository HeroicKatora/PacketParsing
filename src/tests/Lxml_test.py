from lxml import etree
from os import listdir
import unittest

class LxmlTest(unittest.TestCase):
    def setUp(self):
        XS = "{http://www.w3.org/2001/XMLSchema}"
        #print('Testing XML validation')
        with open('./template.xml') as template:
            tempTree = etree.parse(template)
        for file in filter(lambda p: p.endswith('.xsd'), listdir('./schemes')):
            location = '/'.join(('.', 'schemes', file))
            with open(location) as xsdFile:
                xsdScheme = etree.parse(xsdFile)
                namespace = xsdScheme.getroot().attrib['targetNamespace']
                #print(namespace, ' namespace found in file ', location)
                importXs = etree.Element(XS+'import')
                importXs.attrib['namespace'] = namespace
                importXs.attrib['schemaLocation'] = location
                tempTree.getroot().append(importXs)
        #print('Constructing template xsd')
        self.templateSchema = etree.XMLSchema(tempTree)
        self.parser = etree.XMLParser(schema=self.templateSchema, attribute_defaults=True, remove_blank_text=True, resolve_entities=True)

    def test_parsing(self):
        #print('Trying to parse an xml with the default libraries')
        tree = etree.parse('./xml/StandardDocument.xml', self.parser)
        #print('Parsing succeeded, verifying result')
        #print(etree.tostring(tree.getroot(), pretty_print=True).decode('UTF-8'))
        #print('Testing element int64')
        int64 = tree.find('{http://github.com/HeroicKatora/PacketParsing}type')
        self.assertIsNotNone(int64)

    def test_complex(self):
        #print('Trying to use more features')
        tree = etree.parse('./xml/IPv4Types.xml', self.parser)
        #print('Parsing succeeded')

class UtilMethodTest(unittest.TestCase):
    def setUp(self):
        with open('./template.xml') as template:
            self.tree = etree.parse(template)

    def test_tag_name(self):
        from src.gpp.xmlparsing.builtin import tag_split
        el = self.tree.getroot()
        self.assertEqual(tag_split(el).basetag, 'schema')

if __name__ == "__main__":
    unittest.main()
