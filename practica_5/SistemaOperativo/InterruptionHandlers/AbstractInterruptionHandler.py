from SistemaOperativo.InterruptionHandlers.util.Process import *
import log

class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

    def contextSwitch(self, pcbcpu, pcbnew):
        pcbcpu.changeState(Process.READY)
        self._kernel.dispatcher.save(pcbcpu)
        self.kernel.scheduler.add(pcbcpu)
        pcbnew.changeState(Process.RUNNING)
        self.kernel.pcbTable._runningPcb = pcbnew
        pageTable = self.kernel.memoryManager.getPageTable(pcbnew.pid)
        self._kernel.dispatcher.load(pcbnew,pageTable)

    def runIfThereIsNext(self):
        if self.kernel.scheduler.hasNext():
            nextPcb = self.kernel.scheduler.getNext()
            pageTable = self.kernel.memoryManager.getPageTable(nextPcb.pid)
            self.kernel.dispatcher.load(nextPcb,pageTable)
            nextPcb.changeState(Process.RUNNING)
            self.kernel.pcbTable._runningPcb = nextPcb

    def expropriateOrSave(self, pcbInPc, pcbNew):
        if self.kernel.scheduler.isToExpropriate(pcbInPc, pcbNew):
            log.logger.info("Estamos en el IF")
            self.contextSwitch(pcbInPc, pcbNew)
        else:
            pcbNew.changeState(Process.READY)
            self.kernel.scheduler.add(pcbNew)

