import os

from PIL import Image
from tagger import ImageTaggerResNet152V2

from shared import ImageRecognitionRequest

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # don't use GPU during the testing

test_image = Image.open("test_image.png").resize((224, 224)).convert("RGB")


def test_ImageTaggerResNet152V2():
    it = ImageTaggerResNet152V2()
    tag = it.tag_image(test_image)

    assert tag is not None


def test_ImageRequestSerializeAndDeserialize():
    """Test, whether the image request succesfully serializes and deserializes"""
    ir = ImageRecognitionRequest(test_image)
    b = ir.tobytes()
    d = ImageRecognitionRequest.frombytes(b)

    # compare images byte by byte
    assert ir.image.tobytes() == d.image.tobytes()
