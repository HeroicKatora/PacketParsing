
from abc import ABCMeta, abstractclassmethod


class PacketLibrary(metaclass=ABCMeta):
    """
    Library documentation class
    """
    @abstractclassmethod
    def schemes(self):
        """
        :return: a collection of (schema, module) pairs added by the library
        """
        pass

    @abstractclassmethod
    def xml(self):
        """
        :return: a collection of xml files contained in the library
        """
        pass

    @abstractclassmethod
    def identifier(self):
        """
        :return: a unique identifier for this packet library
        """


class SimpleLibrary(PacketLibrary):
    def __init__(self, identifier, schemes, xmls):
        self.identifier_ = identifier
        self.schemes_ = schemes
        self.xmls_ = xmls
    def schemes(self):
        return self.schemes_
    def xml(self):
        return self.xmls_
    def identifier(self):
        return self.identifier_


class PacketDocument:
    def __init__(self, xml_tree, namespaces):
        self.xml_tree = xml_tree
        self.namespace_implementors = namespaces
        self.imported_objects = dict()
        self.all_objects = dict()
        self.type = dict()
        self.io = dict()
        self.display = dict()
        self.parser = dict()
        self.printer = dict()
        self.reader = dict()
        self.writer = dict()
        self.global_module = dict()
        self.packet = dict()


class PacketParser:
    def __init__(self, xml_registry, documents_map):
        self.namespace_implementors = {l: d for l, d in xml_registry.namespace_implementors.items()}
        self.documents_map = documents_map
