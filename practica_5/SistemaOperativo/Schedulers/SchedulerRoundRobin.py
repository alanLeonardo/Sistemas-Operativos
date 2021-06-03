from SistemaOperativo.Schedulers.AbstractSchedule import AbstractSchedule


class SchedulerRoundRobin(AbstractSchedule):

    def add(self, pcb):
        self._readyQueue.addQueue(pcb)

    def setQuantum(self, quantum):
        HARDWARE.timer.quantum = quantum

    def resetTimer(self):
        HARDWARE.timer.reset()

    def isToExpropriate(self, pcbInPC, pcbNew):
        log.logger.error("-- Method was redefined in class in class {classname}".format(classname=self.__class__.__name__))
