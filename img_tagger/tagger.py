from abc import ABC, abstractmethod

import numpy as np

# Keras has to be imported after the Tensorflow is properly setup (in regards to
# VRAM usage etc.)
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.resnet_v2 import (
    ResNet152V2,
    decode_predictions,
    preprocess_input,
)
from tensorflow.keras.preprocessing import image

from tag import ImageTag

# If there is a GPU available, enable memory_growth
physical_devices = tf.config.list_physical_devices("GPU")
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)


class ImageTagger(ABC):
    @abstractmethod
    def tag_image(self, img: Image.Image) -> ImageTag:
        pass


class ImageTaggerResNet152V2(ImageTagger):
    def __init__(self):
        self.model = ResNet152V2(weights="imagenet")

    def tag_image(self, img: Image.Image) -> ImageTag:
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        preds = self.model.predict(x)
        # decode the results into a list of tuples (class, description, probability)
        # (one such list for each sample in the batch)
        decoded_preds = decode_predictions(preds, top=3)[0]
        # print('Predicted:', decoded_preds)
        return ImageTag(decoded_preds)
