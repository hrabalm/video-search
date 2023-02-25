import io
import pickle

import dramatiq.encoder
import lz4.block
import pyzstd


class ZstdPickleEncoder(dramatiq.encoder.Encoder):
    """Pickles messages and compresses them using Zstd"""

    def __init__(self, compression_level=1):
        self._compression_level = compression_level

    def encode(self, data: dramatiq.encoder.MessageData) -> bytes:
        with io.BytesIO() as f:
            pickle.dump(data, f)
            return pyzstd.compress(f.getvalue(), self._compression_level)

    def decode(self, data: bytes) -> dramatiq.encoder.MessageData:
        with io.BytesIO(pyzstd.decompress(data)) as f:
            return pickle.load(f)


class Lz4PickleEncoder(dramatiq.encoder.Encoder):
    """Pickles messages and compresses them using LZ4"""

    def __init__(self, compression_level=1):
        self._compression_level = compression_level

    def encode(self, data: dramatiq.encoder.MessageData) -> bytes:
        with io.BytesIO() as f:
            pickle.dump(data, f)
            return lz4.block.compress(f.getvalue(), compression=self._compression_level)

    def decode(self, data: bytes) -> dramatiq.encoder.MessageData:
        with io.BytesIO(lz4.block.decompress(data)) as f:
            return pickle.load(f)
