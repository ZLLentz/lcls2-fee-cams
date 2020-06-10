import sys
import time

from ophyd.areadetector.detectors import DetectorBase
from ophyd.areadetector.cam import CamBase
from ophyd.areadetector.plugins import ImagePlugin
from ophyd.device import Component as Cpt
from ophyd.log import config_ophyd_logging
from PIL import Image


class ScreenShot(DetectorBase):
    cam = Cpt(CamBase, ':CAM:')
    image = Cpt(ImagePlugin, ':CAM:DATA1:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs[self.cam.acquire] = 1


def main(pvbase, filename):
    # config_ophyd_logging(level=20)
    print('Connecting to PVs')
    screenshot = ScreenShot(pvbase, name='screenshot')
    print('Starting image stream')
    try:
        screenshot.stage()
        time.sleep(0.25)
        print('Getting image')
        image = Image.fromarray(screenshot.image.image)
    except Exception:
        raise
    finally:
        print('Cleaning up')
        screenshot.unstage()
    print('Saving image')
    image.save(filename)
    print('Showing image')
    image.show()
    print('Exiting')


if __name__ == '__main__':
    pvbase, filename = sys.argv[1:]
    main(pvbase, filename)
