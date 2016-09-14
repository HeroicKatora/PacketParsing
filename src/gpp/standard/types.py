from collections import namedtuple
from json import loads
from parse import parse
from re import match
from bitstring import pack

from ..bitstream import rollback
from ..interfaces import PacketType, PacketDisplay, PacketModule

EnumValue = namedtuple('EnumValue', 'mnemonic parsed')


class Enumeration(PacketType):
    def __init__(self, valuelist, fallback=None):
        PacketType.__init__(self)
        self.fallback = fallback
        self.valuelist = valuelist

    def parse(self, string):
        pass

    def print(self, data):
        pass

    def read(self, bitstr):
        pass

    def write(self, bitstr, data):
        pass


class IntegralDisplay(PacketDisplay):
    def __init__(self, formatstring='{:d}'):
        PacketDisplay.__init__(self)
        self.formatstring = formatstring

    def parse(self, string):
        try:
            return parse(self.formatstring, string).fixed[0]
        except:
            return None

    def print(self, data):
        return self.formatstring.format(data)


class IntegralType(IntegralDisplay, PacketType):
    def __init__(self, subtype, formatstring='{:d}'):
        PacketType.__init__(self)
        IntegralDisplay.__init__(self, formatstring)
        self.subtype = subtype
        self.length = integralLength(subtype)
        self.bitstringformat = 'uint:{:d}'.format(self.length)

    def read(self, bitstr):
        return bitstr.read(self.bitstringformat)

    def write(self, bitstr, data):
        bitstr.append(pack(self.bitstringformat, data))


def integralLength(typeid):
    if typeid in {'char', 'byte', 'uint8'}:
        return 8
    if typeid in {'short', 'uint16'}:
        return 16
    if typeid in {'int', 'uint32'}:
        return 32
    if typeid in {'long', 'uint64'}:
        return 64
    le = match('([0-9]*)bit', typeid)
    return int(le.groups()[0])


class Field(PacketModule):
    def __init__(self, type, displayname):
        self.type = type
        self.displayname = displayname

    def read(self, *args, **kwars):
        return self.type.read(*args, **kwars)

    def write(self, *args, **kwars):
        return self.type.write(*args, **kwars)

    def parse(self, *args, **kwars):
        return self.type.parse(*args, **kwars)

    def print(self, *args, **kwars):
        return self.type.print(*args, **kwars)



class Sequence(PacketModule):
    def __init__(self, submodules):
        PacketType.__init__(self)
        self.submodules = submodules

    def read(self, bitstream):
        with rollback(bitstream):
            return {mod.name: mod.read(bistream) for mod in self.submodules}

    def write(self, bitstream, data):
        for mod in self.submodules:
            mod.write(bistream, data[mod.name])

    def parse(self, string):
        asjson = loads(string)
        return {mod.name: mod.parse(asjson[mod.name]) for mod in self.submodules}

    def print(self, data):
        asjson = {mod.name: mod.print(data[mod.name]) for mod in self.submodules}
        return dumps(asjson)
