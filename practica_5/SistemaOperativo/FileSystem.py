from Hardware.hardware import *


class FileSystem:

    def __init__(self):
        self._programs = dict()

    @property
    def programs(self):
        return self._programs

    def write(self, path, program):
        self._programs[path] = program

    def read(self, path):
        return self.programs.get(path)
