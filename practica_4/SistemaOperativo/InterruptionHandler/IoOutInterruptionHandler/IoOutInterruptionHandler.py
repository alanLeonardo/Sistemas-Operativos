from SistemaOperativo.InterruptionHandler.AbstractInterruptionHandler.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.PCB.PCB import *
from SistemaOperativo.InterruptionHandler.util.Process import *
from SistemaOperativo.PCB.PCB import *
import log

class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.ioDeviceController.getFinishedPCB()
        pcbInCpu = self.kernel.pcbTable.runningPcb

        if self.kernel.pcbTable.runningPcb:
            pcbInCpu.changeState(Process.READY)
            self._kernel.scheduler.add(pcbInCpu)
        else:
            pcb.changeState(Process.RUNNING)
            self._runningPcb = pcb
            self.kernel.dispatcher.load(pcb)

