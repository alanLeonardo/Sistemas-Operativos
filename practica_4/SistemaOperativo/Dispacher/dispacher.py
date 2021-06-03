from Hardware.hardware import *


class Dispatcher:
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def load(self, pcb):
        HARDWARE.mmu._baseDir = pcb.baseDir
        HARDWARE.cpu._pc = pcb.pc
        HARDWARE.timer.reset()

    def save(self, pcb):
        pcb.updatePC(HARDWARE.cpu.pc)
        HARDWARE.cpu.pc = -1
