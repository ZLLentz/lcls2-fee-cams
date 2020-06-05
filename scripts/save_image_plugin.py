import sys

from ophyd.areadetector.plugins import TIFFPlugin
from ophyd.log import config_ophyd_logging
from ophyd.utils import set_and_wait


def create_plugin(imager_prefix):
    return TIFFPlugin(imager_prefix + ':CAM:TIFF1:', name='tiff')


def setup_plugin(plugin, filename):
    set_and_wait(plugin.file_template, '%s%s_%3.3d.tif')
    set_and_wait(plugin.file_path, '/reg/neh/home/zlentz/images/')
    set_and_wait(plugin.file_name, filename)
    set_and_wait(plugin.auto_increment, 1)


def take_image(plugin, filename=None):
    if filename is not None:
        set_and_wait(plugin.file_name, filename)
    set_and_wait(plugin.capture, 1)
    plugin.write_file.put(1)


def main(args):
    config_ophyd_logging(level="DEBUG")
    plugin = create_plugin(args[0])
    setup_plugin(plugin, args[1])
    take_image(plugin)


if __name__ == '__main__':
    main(sys.argv[1:])
