# import av
import pika
from constants_test import HOST, QUEUE_NAME
from PIL import Image

from shared import ImageRecognitionRequest

img = Image.open("test_image.png").convert("RGB").resize((224, 224))


def create_test_message():
    msg = ImageRecognitionRequest(img).tobytes()

    return msg


connection = pika.BlockingConnection(pika.ConnectionParameters(HOST))
channel = connection.channel()

channel.queue_declare(QUEUE_NAME)

msg = create_test_message()

COUNT = 5

for _ in range(COUNT):
    channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=msg)

connection.close()
