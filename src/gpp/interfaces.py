"""
Created on 03.07.2016

@author: andreas
"""
from abc import ABCMeta, abstractclassmethod


class PacketReadable(metaclass=ABCMeta):
    @abstractclassmethod
    def read(self, bitstream):
        pass

class PacketWriteable(metaclass=ABCMeta):
    @abstractclassmethod
    def write(self, bitstream):
        pass


class PacketPrintable(metaclass=ABCMeta):
    @abstractclassmethod
    def print(self, charstream):
        pass

class PacketParseable(metaclass=ABCMeta):
    @abstractclassmethod
    def parse(self, charstream):
        pass

class PacketIO(PacketReadable, PacketWriteable):
    pass

class PacketDisplay(PacketPrintable, PacketParseable):
    pass

class PacketType(PacketIO, PacketDisplay):
    pass

class PacketModule(metaclass=ABCMeta):
    @abstractclassmethod
    def submodules():
        pass

    @abstractclassmethod
    def content():
        pass

    def __call__(self):
        return self.content()
