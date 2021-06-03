from Hardware.hardware import *
class Loader():

    def __init__(self):
        self._nextDir= 0

    def load_program(self, program):
        # loads the program in main memory
        baseDir: int = self._nextDir
        for index in program.instructions:
            HARDWARE.memory.write(self._nextDir, index)
            self._nextDir+=1
        return baseDir