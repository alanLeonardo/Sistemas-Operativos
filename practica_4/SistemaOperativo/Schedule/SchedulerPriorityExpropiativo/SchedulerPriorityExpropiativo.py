import log
from SistemaOperativo.InterruptionHandler.util.Process import *
from Hardware.hardware import *
from SistemaOperativo.ReadyQueue.readyQueue import *
from SistemaOperativo.Schedule.AbstractSchedule.AbstractSchedule import AbstractSchedule


class SchedulerPriorityExpropiativo(AbstractSchedule):

    def add(self,pcb):
        self.readyQueue.addQueue(pcb)
        self.readyQueue.queue.sort(key=lambda p: p.priority)

    def isToExpropriate(self, pcbInPC, pcbNew):
        return pcbInPC.priority > pcbNew.priority
