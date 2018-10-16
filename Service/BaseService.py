import os
import sys


def get_root_path():
    if sys.path[0] == os.getcwd():
        p = sys.path[0]
    else:
        p = sys.path[1]
    paste_path = os.path.join(p, 'pastefile')
    try:
        os.mkdir(paste_path)
    except BaseException as e:
        print("Paste folder already created")
    return p


def get_db_path():
    if sys.path[0] == os.getcwd():
        p = sys.path[0]
    else:
        p = sys.path[1]
    return os.path.join(p, 'pastebin.db')
