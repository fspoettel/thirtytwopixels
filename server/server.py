import io
import os
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import syslog
from threading import Timer
import time
from PIL import Image
import zmq

IS_PRODUCTION = os.uname()[4][:3] == "arm"
# shutting down/sleeping OS does not invoke `ncmpcpp.execute_on_player_state_change`
# we want a timeout that ensures that our matrix is cleared
# after a certain amount of time w/o a song or state change
MATRIX_INACTIVITY_TIMEOUT = 4 * 60 * 60


class MockMatrix:
    def Clear(self):
        print("Clearing matrix")

    def SetImage(self, im):
        byte_io = io.BytesIO()
        im.save(byte_io, format="PPM")
        print("[{}] {}".format(time.time(), byte_io.getbuffer().nbytes))


def matrix_factory(width):
    options = RGBMatrixOptions()
    # `pwm` requires small hardware mod but greatly improves flicker
    options.hardware_mapping = "adafruit-hat-pwm"
    options.chain_length = 1
    options.rows = width
    # these settings work well on a zero wh
    options.gpio_slowdown = 0
    options.pwm_lsb_nanoseconds = 100
    options.pwm_dither_bits = 1
    matrix = RGBMatrix(options=options)
    return matrix


class Panel:
    def __init__(self):
        self.matrix = matrix_factory(32) if IS_PRODUCTION else MockMatrix()
        self.prev_byte_io = None
        self.timeout = None

    def clear(self):
        self.prev_byte_io = None
        self.stop_inactivity_timer()
        self.matrix.Clear()

    def clear_if_unchanged(self, current_byte_io):
        if current_byte_io == self.prev_byte_io:
            self.clear()

    def stop_inactivity_timer(self):
        if self.timeout:
            self.timeout.cancel()
            self.timeout = None

    def start_inactivity_timer(self, byte_io):
        self.stop_inactivity_timer()
        self.timeout = Timer(MATRIX_INACTIVITY_TIMEOUT, self.clear_if_unchanged, [byte_io])
        self.timeout.start()

    def draw(self, message):
        byte_io = io.BytesIO(message)

        if not compare_bytes(self.prev_byte_io, byte_io):
            self.prev_byte_io = byte_io
            im = Image.open(byte_io)
            self.matrix.SetImage(im.convert("RGB"))
            self.start_inactivity_timer(byte_io)


def get_bytes(byte_io):
    return list(bytes(byte_io.getvalue()))


def is_byte_io(val):
    return isinstance(val, io.BytesIO)


def compare_bytes(a, b):
    return is_byte_io(a) and is_byte_io(b) and get_bytes(a) == get_bytes(b)


panel = Panel()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    try:
        message = socket.recv()
        if message == b"UUDDLRLRBA":
            panel.clear()
        else:
            panel.draw(message)
        socket.send(b"1")
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, str(e))
        print(e)
        try:
            socket.send(b"0")
        except:
            pass
