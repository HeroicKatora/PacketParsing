"""
Created on 03.07.2016

@author: andreas
"""
from abc import ABCMeta, abstractclassmethod


class PacketReader(metaclass=ABCMeta):
    @abstractclassmethod
    def read(self, bitstream):
        pass

class PacketWriter(metaclass=ABCMeta):
    @abstractclassmethod
    def write(self, bitstream, data):
        pass

class PacketPrinter(metaclass=ABCMeta):
    @abstractclassmethod
    def print(self, data):
        pass

class PacketParser(metaclass=ABCMeta):
    @abstractclassmethod
    def parse(self, string):
        pass

class PacketConstructer(metaclass=ABCMeta):
    @abstractclassmethod
    def empty(self):
        pass

class PacketIO(PacketReader, PacketWriter):
    pass

class PacketDisplay(PacketPrinter, PacketParser):
    pass

class PacketType(PacketIO, PacketDisplay):
    pass

class PacketModule(PacketType):
    pass


class PacketData(metaclass=ABCMeta):
    def __init__(self, type):
        self.type = type

    @abstractclassmethod
    def submodules():
        pass

    @abstractclassmethod
    def content():
        pass

    def __call__(self):
        return self.content()
