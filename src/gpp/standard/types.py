from collections import namedtuple
from ..interfaces import PacketType, PacketDisplay

EnumValue = namedtuple('EnumValue', 'mnemonic parsed')


class Enumeration(PacketType):
    def __init__(self, valuelist, fallback=None):
        super().__init__(self)

class DisplayIntegral(PacketDisplay):
    pass


class TypeIntegral(DisplayIntegral, PacketType):
    pass
