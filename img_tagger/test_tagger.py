from tagger import *
from PIL import Image

test_image = Image.open('test_image.png').resize((224, 224))


def test_ImageTaggerResNet152V2():
    it = ImageTaggerResNet152V2()
    it.tag_image(test_image)

    assert True
