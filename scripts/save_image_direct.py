import sys

from PIL import Image
from ophyd.areadetector.plugins import ImagePlugin


def main(pvbase, filename):
    image_plugin = ImagePlugin(pvbase + ':CAM:DATA1:',
                               name='image_plugin')
    image = Image.fromarray(image_plugin.image)
    image.save(filename)
    image.show()


if __name__ == '__main__':
    pvbase, filename = sys.argv[1:]
    main(pvbase, filename)
