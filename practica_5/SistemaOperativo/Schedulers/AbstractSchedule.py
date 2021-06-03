from Hardware.hardware import *
from SistemaOperativo.readyQueue import *

class AbstractSchedule():

    def __init__(self):
        self._readyQueue = ReadyQueue()

    @property
    def readyQueue(self):
        return self._readyQueue

    def hasNext(self):
        return len(self._readyQueue.queue) != 0


    def add(self, pcb):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

    def getNext(self):
        return self._readyQueue.queue.pop(0)

    def isToExpropriate(self, pcbInPC, pcbNew):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))
