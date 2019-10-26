import os
import time

from modules.event import Event


class Pipe:
    def __init__(self):
        self.read_path = "/Users/zhouziyang/Documents/LMU/Studium/Informatik/Bachelorarbeit/Repo/Vis-Tuning/pipe" \
                         "/fasttext.pipe"

    def makePipe(self):
        try:
            os.mkfifo(self.read_path)
        except OSError as e:
            print("mkfifo error", e)
        return 0

    def openPipe(self):
        rf = os.open(self.read_path, os.O_RDONLY)
        print("os.open finished")

        while True:
            data = os.read(rf, 1024)
            if len(data) == 0:
                print("nodata")
                time.sleep(1)
            print(data)
            Event('append', "testtest")


pipe = Pipe()
# pipe.makePipe()
pipe.openPipe()
