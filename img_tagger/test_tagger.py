import os

from PIL import Image
from shared import ImageRequest

from tagger import ImageTaggerResNet152V2

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # don't use GPU during the testing

test_image = Image.open("test_image.png").resize((224, 224)).convert("RGB")


def test_ImageTaggerResNet152V2():
    it = ImageTaggerResNet152V2()
    it.tag_image(test_image)

    assert True


def test_ImageRequestSerializeAndDeserialize():
    """Test, whether the image request succesfully serializes and deserializes
    """
    ir = ImageRequest(test_image)
    b = ir.tobytes()
    d = ImageRequest.frombytes(b)

    # compare images byte by byte
    assert ir.img.tobytes() == d.img.tobytes()
