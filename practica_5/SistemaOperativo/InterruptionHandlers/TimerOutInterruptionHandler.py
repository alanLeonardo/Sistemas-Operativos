from SistemaOperativo.InterruptionHandlers.AbstractInterruptionHandler import \
    AbstractInterruptionHandler


class TimerOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        if self.kernel.scheduler.hasNext():
            nextPCB = self.kernel.scheduler.getNext()
            pcbCPU = self.kernel.pcbTable.runningPcb
            self.contextSwitch(pcbCPU, nextPCB)
        else:
            self.kernel.scheduler.resetTimer()
