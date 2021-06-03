from SistemaOperativo.InterruptionHandler.AbstractInterruptionHandler.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.PCB.PCB import *
from SistemaOperativo.InterruptionHandler.util.Process import *
from SistemaOperativo.PCB.PCB import *
import log

class TimerOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        if self.kernel.scheduler.hasNext():
            nextPCB = self.kernel.scheduler.getNext()
            pcbCPU = self.kernel.pcbTable.runningPcb
            self.contextSwitch(pcbCPU, nextPCB)
        else:
            self.kernel.scheduler.resetTimer()
