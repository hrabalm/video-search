from PIL import Image
import pika
import logging
import bson

from tagger import ImageTaggerResNet152V2
from shared import ImageRequest

from constants_test import HOST, QUEUE_NAME

logger = logging.getLogger()

tagger = ImageTaggerResNet152V2()


def callback(ch, method, properties, body):
    print(f" [x] Received {body[:50]}")
    img: Image.Image = ImageRequest.frombytes(body).img

    tag = tagger.tag_image(img)
    print(f" [x] Computed tag: {tag}")

    ch.basic_ack(delivery_tag=method.delivery_tag)


def server_loop():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=HOST)
    )
    channel = connection.channel()

    channel.queue_declare(QUEUE_NAME)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)
    channel.start_consuming()
