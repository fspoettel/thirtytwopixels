import io
import syslog
from PIL import Image
import zmq

def get_bytes(byte_io):
    return list(bytes(byte_io.getvalue()))

def is_byte_io(val):
    return isinstance(val, io.BytesIO)

def compare_bytes(a, b):
    return is_byte_io(a) and is_byte_io(b) and get_bytes(a) == get_bytes(b)

class Panel:
    def __init__(self):
        self.prev_byte_io = None

    def draw(self, message):
        byte_io = io.BytesIO(message)

        if not compare_bytes(self.prev_byte_io, byte_io):
            self.prev_byte_io = byte_io
            im = Image.open(byte_io)
            im.show()


panel = Panel()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    try:
        message = socket.recv()
        panel.draw(message)
        socket.send(b"1")
    except Exception as e:
        syslog.syslog(syslog.LOG_ERR, str(e))
        print(e)
        try:
            socket.send(b"0")
        except:
            pass
