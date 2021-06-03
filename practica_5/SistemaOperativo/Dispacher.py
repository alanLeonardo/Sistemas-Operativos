from Hardware.hardware import *


class Dispatcher:

    def load(self, pcb, page_table_del_pcb):
        HARDWARE.mmu.resetTLB()
        if page_table_del_pcb:
            for index, element in enumerate(page_table_del_pcb):
                HARDWARE.mmu.setPageFrame(element.page, element.frame)
            HARDWARE.cpu._pc = pcb.pc
            HARDWARE.timer.reset()



    def save(self, pcb):
        pcb.updatePC(HARDWARE.cpu.pc)
        HARDWARE.cpu._pc = -1
