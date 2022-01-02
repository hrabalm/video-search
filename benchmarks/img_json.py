import json
import bson
import base64
import lz4.frame
from os import times
import zlib
from PIL import Image
import timeit

img = Image.open('test_image.png').convert('RGB')
small_img = img.resize((224, 224))

img = img.tobytes()
small_img = small_img.tobytes()

def to_json(img: bytes) -> bytes:
    return json.dumps({'data': base64.b64encode(img).decode('utf-8')}).encode('utf-8')

def to_bson(img: bytes) -> bytes:
    return bson.dumps({'data': img})

def to_binary_json_zlib(img: bytes) -> bytes:
    return zlib.compress(to_json(img), level=1)

def to_binary_json_lz4(img: bytes) -> bytes:
    return lz4.frame.compress(to_json(img))

def print_size(name: str, img: bytes):
    orig = len(img)/1024
    json = len(to_json(img))/1024
    bson = len(to_bson(img))/1024
    zlib = len(to_binary_json_zlib(img))/1024
    print(f"{name}, orig={orig}kB, json={json}kB, bson={bson}kb, zlib={zlib}kB, compr={zlib/json}")

print("Size comparisons:")
print_size("img", img)
print_size("small_img", small_img)

def benchmark(funcname: str, imgvar: str, number=2000):
    statement = f"{funcname}({imgvar})"
    ms = timeit.timeit(statement, globals=globals(), number=number)
    print(f"{funcname}({imgvar}) x {number} = {ms}s")

benchmark('to_json', 'img')
benchmark('to_bson', 'img')

# benchmark('to_binary_json_zlib', 'img')
benchmark('to_binary_json_lz4', 'img')
benchmark('to_json', 'small_img')
benchmark('to_bson', 'small_img')
# benchmark('to_binary_json_zlib', 'small_img')
benchmark('to_binary_json_lz4', 'small_img')

# conclusions LZ4 is fine, zlib significantly hurts performance
