from SistemaOperativo.InterruptionHandler.AbstractInterruptionHandler.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.InterruptionHandler.util.Process import *
import log

class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        log.logger.info(" Program Finished ")

        pcbRunning = self.kernel.pcbTable._runningPcb
        pcbRunning.changeState(Process.TERMINATED)
        self.kernel.dispatcher.save(pcbRunning)

        self.kernel.pcbTable._runningPcb = None

        self.runIfThereIsNext()

