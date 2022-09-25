from typing import BinaryIO

import av
import pika


def process_video(file: BinaryIO):
    container = av.open(file)

    for frame in container.decode(video=0):
        resized_frame = frame.to_image().resize((224, 224))
        yield resized_frame


def index_video():
    pass


connection = pika.BlockingConnection("localhost")
channel = connection.channel()

connection.close()
