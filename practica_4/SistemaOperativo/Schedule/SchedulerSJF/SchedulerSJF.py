import log
from SistemaOperativo.InterruptionHandler.util.Process import *
from Hardware.hardware import *
from SistemaOperativo.ReadyQueue.readyQueue import *
from SistemaOperativo.Schedule.AbstractSchedule.AbstractSchedule import AbstractSchedule


class SchedulerSJF(AbstractSchedule):

    def add(self,pcb):
        self._readyQueue.queue.append(pcb)
        self._readyQueue.queue.sort(key=lambda p: p.cantidadTotalDeProcesos)

    def isToExpropriate(self, pcbInPC, pcbNew):
        return pcbInPC.cantidadTotalDeProcesos > pcbNew.cantidadTotalDeProcesos

