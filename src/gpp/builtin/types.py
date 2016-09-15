from ..interfaces import PacketType


class Type(PacketType):
    def __init__(self, name, reader, writer, parser, printer):
        self.name = name
        self.reader, self.writer = reader, writer
        self.parser, self.printer = parser, printer

    def read(self, *args, **kwars):
        return self.reader.read(*args, **kwars)

    def write(self, *args, **kwars):
        return self.writer.write(*args, **kwars)

    def parse(self, *args, **kwars):
        return self.parser.parse(*args, **kwars)

    def print(self, *args, **kwars):
        return self.printer.print(*args, **kwars)

class Submodule(PacketType):
    def __init__(self, name, module):
        PacketType.__init__(self)
        self.name = name
        self.module = module

    def read(self, *args, **kwargs):
        return self.module.read(*args, **kwargs)

    def write(self, *args, **kwargs):
        return self.module.write(*args, **kwargs)

    def parse(self, *args, **kwargs):
        return self.module.parse(*args, **kwargs)

    def print(self, *args, **kwargs):
        return self.module.print(*args, **kwargs)
