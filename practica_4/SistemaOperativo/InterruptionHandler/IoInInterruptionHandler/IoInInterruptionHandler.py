from SistemaOperativo.InterruptionHandler.AbstractInterruptionHandler.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.PCB.PCB import *
from SistemaOperativo.InterruptionHandler.util.Process import *
from SistemaOperativo.PCB.PCB import *
import log

class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        self.kernel.pcbTable._runningPcb.changeState(Process.WAITING)

        pcb = self.kernel.pcbTable._runningPcb

        self.kernel.dispatcher.save(pcb)

        self.kernel.pcbTable._runningPcb = None
        self.kernel.ioDeviceController.runOperation(pcb, operation)
        log.logger.info(pcb.pid)

        self.runIfThereIsNext()

