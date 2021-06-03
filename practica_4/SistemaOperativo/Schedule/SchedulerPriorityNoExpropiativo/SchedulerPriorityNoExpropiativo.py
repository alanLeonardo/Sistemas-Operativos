import log
from SistemaOperativo.InterruptionHandler.util.Process import *
from Hardware.hardware import *
from SistemaOperativo.ReadyQueue.readyQueue import *
from SistemaOperativo.Schedule.AbstractSchedule.AbstractSchedule import AbstractSchedule


class SchedulerPriorityNoExpropiativo(AbstractSchedule):

   def add(self, pcb):
       self.readyQueue.addQueue(pcb)
       self.readyQueue.queue.sort(key=lambda p: p.priority)

   def isToExpropriate(self, pcbInPC, pcbNew):
       log.logger.error("-- Method was redefined in class in class {classname}".format(classname=self.__class__.__name__))

