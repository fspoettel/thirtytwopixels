#!/usr/bin/env python3
import syslog
from client.matrix import Matrix
from client.mpd import get_cover

if __name__ == "__main__":
    try:
        matrix = Matrix([32, 32])
        matrix.show(get_cover())
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, str(e))
