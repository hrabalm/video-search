# TODO: Use Resnet 152 instead
import abc

import numpy as np
from PIL import Image

# Keras has to be imported after the Tensorflow is properly setup (in regards to
# VRAM usage etc.)
from tensorflow.keras.applications.resnet50 import (ResNet50,
                                                    decode_predictions,
                                                    preprocess_input)
from tensorflow.keras.preprocessing import image


class ImageTagger(abc.ABC):
    pass

class ImageTaggerResNet50(ImageTagger):
    pass


def tag():
    pass
