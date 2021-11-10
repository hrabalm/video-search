import os

from PIL import Image

from tagger import *

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # don't use GPU during the testing

test_image = Image.open('test_image.png').resize((224, 224)).convert('RGB')


def test_ImageTaggerResNet152V2():
    it = ImageTaggerResNet152V2()
    tag = it.tag_image(test_image)

    print(tag)

    assert True
