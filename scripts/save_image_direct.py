import sys
import time

import imageio
import numpy as np
from ophyd.areadetector.detectors import DetectorBase
from ophyd.areadetector.cam import CamBase
from ophyd.areadetector.plugins import ImagePlugin
from ophyd.device import Component as Cpt
from ophyd.signal import EpicsSignalRO
from ophyd.log import config_ophyd_logging


class ScreenShot(DetectorBase):
    cam = Cpt(CamBase, ':CAM:')
    image = Cpt(ImagePlugin, ':CAM:DATA1:')
    bit_depth = Cpt(EpicsSignalRO, ':CAM:BitsPerPixel_RBV')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stage_sigs[self.cam.acquire] = 1


def get_image(screenshot):
    # Set type based on bit depth
    bit_depth = screenshot.bit_depth.get()
    image = screenshot.image.image
    if bit_depth <= 8:
        # Use 8-bit pixels
        return (image * 2**8/image.max()).astype(np.uint8)
    else:
        # Use 16-bit pixels
        return (image * 2**16/image.max()).astype(np.uint16)


def main(pvbase, filename):
    # config_ophyd_logging(level=20)
    print('Connecting to PVs')
    screenshot = ScreenShot(pvbase, name='screenshot')
    print('Starting image stream')
    try:
        screenshot.stage()
        time.sleep(0.25)
        print('Getting image')
        image = get_image(screenshot)
    except Exception:
        raise
    finally:
        print('Cleaning up')
        screenshot.unstage()
    print('Saving image')
    imageio.imwrite(filename, image)
    print('Exiting')


if __name__ == '__main__':
    pvbase, filename = sys.argv[1:]
    main(pvbase, filename)
