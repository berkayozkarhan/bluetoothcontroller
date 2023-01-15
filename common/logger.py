from datetime import datetime
import threading
import json
import uuid


class Logger:
    """
    c: console
    f: file
    * Multiple available. example : "cf"
    """

    def __init__(self, app_name, lock: threading.Lock, file_name=None):
        self.app_name = app_name
        self.file_name = file_name
        self.lock = lock

        if self.file_name is None:
            self.file_name = self.app_name + ".log"

    def log_direct(self, log_data, log_type):
        if "f" in log_type:
            self.lock.acquire()
            with open(self.file_name, 'a') as log_file:
                log_file.write(log_data)
            self.lock.release()

        if "c" in log_type:
            print(log_data)


