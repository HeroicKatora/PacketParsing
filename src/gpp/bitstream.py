from contextlib import contextmanager


@contextmanager
def rollback(bitstream):
    pos = bitstream.pos
    try:
        yield bitstream
    except:
        bitstream.pos = pos
        raise
