#!/usr/bin/env python3
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import syslog
from client.matrix_connection import MatrixConnection
from client.mpd import get_cover

if __name__ == "__main__":
    try:
        matrix = MatrixConnection([32, 32])
        matrix.show(get_cover())
    except Exception as e:
        syslog.syslog(syslog.LOG_INFO, str(e))
