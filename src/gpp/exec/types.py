"""
Created on 25.07.2016

@author: andreas
"""
from ..interfaces import PacketType
class Type(PacketType):
    def __init__(self, name, reader, writer, parser, printer):
        self.name = name
        self.reader, self.writer = reader, writer
        self.parser, self.printer = parser, printer

    def read(self, *args):
        return self.reader.read(*args)

    def write(self, *args):
        return self.writer.write(*args)

    def parse(self, *args):
        return self.parser.parse(*args)

    def print(self, *args):
        return self.printer.print(*args)
