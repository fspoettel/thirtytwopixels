#!/usr/bin/env python3
import os
import syslog
from client.matrix import Matrix

if __name__ == "__main__":
    try:
        if os.getenv("MPD_PLAYER_STATE") == "stop":
            matrix = Matrix([32, 32])
            matrix.clear()
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, str(e))
