from abc import ABC, abstractmethod
from typing import Collection

import numpy as np

# Keras has to be imported after the Tensorflow is properly setup (in regards
# to VRAM usage etc.)
import tensorflow as tf
from PIL import Image
from shared import ImageTags, Tag
from tensorflow.keras.applications.resnet_v2 import (
    ResNet152V2,
    decode_predictions,
    preprocess_input,
)
from tensorflow.keras.preprocessing import image

# If there is a GPU available, enable memory_growth
physical_devices = tf.config.list_physical_devices("GPU")
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


class ImageTagger(ABC):
    @abstractmethod
    def tag_image(self, img: Image.Image) -> ImageTags:
        pass

    @abstractmethod
    def tag_images(self, images: Collection[Image.Image]) -> list[ImageTags]:
        pass


class ImageTaggerResNet152V2(ImageTagger):
    def __init__(self):
        self.source = "ResNet152V2"
        self.model = ResNet152V2(weights="imagenet")

    def tag_image(self, img: Image.Image) -> ImageTags:  # FIXME: to be removed
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = self.model.predict(x)
        # decode the results into a list of tuples (class, description,
        # probability), one such list for each sample in the batch
        decoded_preds = decode_predictions(preds, top=3)[0]
        # print('Predicted:', decoded_preds)
        # print(decoded_preds)
        return ImageTags(
            tags=[Tag(id, name, conf, self.source) for id, name, conf in decoded_preds]
        )

    def tag_images(self, images: Collection[Image.Image]):
        images = [image.img_to_array(x) for x in images]
        images = [preprocess_input(x) for x in images]

        preds = self.model.predict(images)
        decoded_preds = decode_predictions(preds, top=3)  # noqa: F841
        return []  # FIXME
