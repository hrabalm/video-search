from abc import ABC, abstractmethod
from typing import Collection

import numpy as np

# Keras has to be imported after the Tensorflow is properly setup (in regards
# to VRAM usage etc.)
import tensorflow as tf
from PIL import Image
from shared import ImageTags
from tensorflow.keras.applications import EfficientNetV2B0
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
    def tag_images(self, images: Collection[Image.Image]) -> list[ImageTags]:
        pass


class ImageTaggerResNet152V2(ImageTagger):
    def __init__(self):
        self.source = "ResNet152V2"
        self.model = ResNet152V2(weights="imagenet")

    def tag_images(self, images: Collection[Image.Image]):
        images = [image.img_to_array(x) for x in images]
        images = [preprocess_input(x) for x in images]
        images = tf.convert_to_tensor(images)

        preds = self.model.predict(images)
        # decode the results into a list of tuples (class, description,
        # probability), one such list for each sample in the batch
        decoded_preds = decode_predictions(preds, top=3)  # noqa: F841
        return []  # FIXME

        # return ImageTags(
        #     tags=[Tag(id,name,conf,self.source) for id, name, conf in decoded_preds]
        # )


class ImageTaggerEfficientNetV2B0(ImageTagger):
    def __init__(self):
        self.source = "EfficientNetV2B0"
        self.model = EfficientNetV2B0(weights="imagenet")

    def tag_images(self, images: Collection[Image.Image]):
        images = [image.img_to_array(x) for x in images]
        # for some strange reason, this drastically improves performance
        images = np.array(images)
        images = tf.convert_to_tensor(images)

        # print(tf.shape(images))  # FIXME

        preds = self.model.predict(images)
        # decode the results into a list of tuples (class, description,
        # probability), one such list for each sample in the batch
        decoded_preds = decode_predictions(preds, top=3)  # noqa: F841

        # print(decoded_preds) # FIXME

        return []  # FIXME

        # return ImageTags(
        #     tags=[Tag(id,name,conf,self.source) for id, name, conf in decoded_preds]
        # )
