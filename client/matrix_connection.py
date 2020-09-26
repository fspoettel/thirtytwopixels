import io
from pathlib import Path
import tempfile
import time
import zmq
from PIL import Image


ZMQ_HOST = "thirtytwopixels.local"
PORT = 5555


class MatrixConnection:
    def __init__(self, socket_addr, size=[32, 32]):
        self.size = size
        self.socket_addr = "tcp://{}:{}".format(ZMQ_HOST, PORT)

        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.setsockopt(zmq.RCVTIMEO, 2000)

    def resize_to_panel(self, path):
        return Image.open(path).convert('RGB').resize(self.size)

    def image_to_bytes(self, im):
        byte_io = io.BytesIO()
        im.save(byte_io, format="PPM")
        return byte_io

    def send_socket_message(self, message):
        try:
            self.socket.connect(self.socket_addr)
            self.socket.send(message)
            res = self.socket.recv()
            self.socket.disconnect(self.socket_addr)
            return res
        except:
            raise ConnectionError("Could not send message to socket")

    def show(self, im_path):
        if not im_path or not im_path.is_file():
            raise ValueError("{} is not a valid file path".format(im_path))

        thumb = self.resize_to_panel(im_path)
        thumb_byte_io = self.image_to_bytes(thumb)
        self.send_socket_message(thumb_byte_io.getbuffer())

    def clear(self):
        self.send_socket_message(b"UUDDLRLRBA")
