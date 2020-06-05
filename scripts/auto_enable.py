import sys

from pcdsdevices.pim import LCLS2ImagerBase


def check_and_update(imager):
    if imager.y_states.removed:
        imager.detector.cam.acquire.put(0)
    else:
        imager.detector.cam.acquire.put(1)


def main(*imager_pvs):
    imagers = []
    for pv in imager_pvs:
        imagers.append(LCLS2ImagerBase(pv, name=pv.lower().replace(':', '_')))
    while True:
        time.sleep(1)
        for imager in imagers:
            check_and_update(imager)


if __name__ == '__main__':
    main(sys.argv[1:])
