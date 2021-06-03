import log
from SistemaOperativo.Schedulers.AbstractSchedule import AbstractSchedule


class SchedulerFIFO(AbstractSchedule):

    def add(self, pcb):
        self._readyQueue.addQueue(pcb)

    def isToExpropriate(self, pcbInPC, pcbNew):
        log.logger.error("-- Method was redefined in class in class {classname}".format(classname=self.__class__.__name__))