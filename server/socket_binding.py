import syslog
import zmq


class SocketBinding:
    def __init__(self, panel):
        self.panel = panel
        self.bind()

    def bind(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

        while True:
            try:
                message = self.socket.recv()
                if message == b"UUDDLRLRBA":
                    self.panel.clear()
                else:
                    self.panel.draw(message)
                self.socket.send(b"1")
            except Exception as e:
                syslog.syslog(syslog.LOG_ERR, str(e))
                print(e)
                try:
                    self.socket.send(b"0")
                except:
                    pass
