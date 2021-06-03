from SistemaOperativo.InterruptionHandlers.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.InterruptionHandlers.util.Process import *


class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.ioDeviceController.getFinishedPCB()
        pcbInCpu = self.kernel.pcbTable.runningPcb

        if self.kernel.pcbTable.runningPcb:
            pcbInCpu.changeState(Process.READY)
            self._kernel.scheduler.add(pcbInCpu)

            self.expropriateOrSave(pcbInCpu, pcb)
        else:
            pcb.changeState(Process.RUNNING)
            self._runningPcb = pcb
            self.kernel.dispatcher.load(pcb)

