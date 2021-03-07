import io
from threading import Timer
from PIL import Image

# shutting down/sleeping OS does not invoke `ncmpcpp.execute_on_player_state_change`
# we want a timeout that ensures that our matrix is cleared
# after a certain amount of time w/o a song or state change
PANEL_INACTIVITY_TIMEOUT = 4 * 60 * 60


def get_bytes(byte_io):
    return list(bytes(byte_io.getvalue()))


def is_byte_io(val):
    return isinstance(val, io.BytesIO)


def compare_bytes(a, b):
    return is_byte_io(a) and is_byte_io(b) and get_bytes(a) == get_bytes(b)


class Panel:
    def __init__(self, matrix):
        self.matrix = matrix
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
        self.timeout = Timer(
            PANEL_INACTIVITY_TIMEOUT, self.clear_if_unchanged, [byte_io]
        )
        self.timeout.start()

    def draw(self, message):
        byte_io = io.BytesIO(message)

        if not compare_bytes(self.prev_byte_io, byte_io):
            self.prev_byte_io = byte_io
            im = Image.open(byte_io)
            self.matrix.SetImage(im.convert("RGB"))
            self.start_inactivity_timer(byte_io)
