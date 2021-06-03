from SistemaOperativo.InterruptionHandlers.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.InterruptionHandlers.util.Process import *
import log


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        log.logger.info(" Program Finished ")
        pid = self.kernel.pcbTable.runningPcb.pid
        pcbRunning = self.kernel.pcbTable._runningPcb
        pcbRunning.changeState(Process.TERMINATED)
        self.kernel.dispatcher.save(pcbRunning)

        self.kernel.pcbTable._runningPcb = None
        self.kernel.memoryManager.removePageTable(pid)

        self.runIfThereIsNext()
