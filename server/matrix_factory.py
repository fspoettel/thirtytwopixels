import io
import os
import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions

IS_PRODUCTION = os.uname()[4][:3] == "arm"


class MockMatrix:
    def Clear(self):
        print("Clearing matrix")

    def SetImage(self, im):
        byte_io = io.BytesIO()
        im.save(byte_io, format="PPM")
        print("[{}] {}".format(time.time(), byte_io.getbuffer().nbytes))


def matrix_factory(width):
    if not IS_PRODUCTION:
        return MockMatrix()

    options = RGBMatrixOptions()
    # `pwm` requires small hardware mod but greatly improves flicker
    options.hardware_mapping = "adafruit-hat-pwm"
    options.chain_length = 1
    options.rows = width
    # these settings work well on a zero wh
    options.gpio_slowdown = 0
    options.pwm_lsb_nanoseconds = 100
    options.pwm_dither_bits = 1
    options.brightness = 35
    options.pixel_mapper_config= "Rotate:90"
    matrix = RGBMatrix(options=options)
    return matrix
