import io
from pathlib import Path
import tempfile
import time
import zmq
from PIL import Image


ZMQ_HOST = "localhost"
PORT = 5555


class Matrix:
    def __init__(self, socket_addr, size=[32, 32]):
        self.size = size
        self.socket_addr = "tcp://{}:{}".format(ZMQ_HOST, PORT)

        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.RCVTIMEO, 2000)

    def resize_to_panel(self, path):
        return Image.open(path).resize(self.size)

    def image_to_bytes(self, im):
        bytearr = io.BytesIO()
        im.save(bytearr, format="PPM")
        return bytearr

    def show(self, im_path):
        if not im_path or not im_path.is_file():
            raise ValueError("{} is not a valid file path".format(im_path))

        thumb = self.resize_to_panel(im_path)
        thumb_bytes = self.image_to_bytes(thumb)

        try:
            self.socket.connect(self.socket_addr)
            self.socket.send(thumb_bytes.getbuffer())
            self.socket.recv()
            self.socket.disconnect(self.socket_addr)
        except:
            raise ConnectionError("Could not send message to socket")
