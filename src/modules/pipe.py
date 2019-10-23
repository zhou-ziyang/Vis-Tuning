import os
import time

from modules.event import Event


class Pipe:

    def __init__(self):
        self.read_path = "static/pipe/fasttext.pipe"

    def make(self):
        try:
            os.mkfifo(self.read_path)
        except OSError as e:
            print("mkfifo error", e)

    def start_reading(self):
        print("reading thread is on")
        rf = os.open(self.read_path, os.O_RDONLY)
        print("os.open finished")

        while True:
            data = os.read(rf, 1024)
            # print(data)
            if len(data) == 0:
                # print("nodata")
                time.sleep(1)
            else:
                data_split = (str(data)).split(',', maxsplit=1)
                try:
                    Event('append', {"update": data_split[1]})
                except Exception:
                    pass