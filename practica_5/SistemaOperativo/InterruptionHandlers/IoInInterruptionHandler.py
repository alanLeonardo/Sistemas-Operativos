from SistemaOperativo.InterruptionHandlers.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.InterruptionHandlers.util.Process import *


class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        self.kernel.pcbTable._runningPcb.changeState(Process.WAITING)

        pcb = self.kernel.pcbTable._runningPcb

        self.kernel.dispatcher.save(pcb)

        self.kernel.pcbTable._runningPcb = None
        self.kernel.ioDeviceController.runOperation(pcb, operation)
        #log.logger.info(pcb.pid)

        self.runIfThereIsNext()

