from SistemaOperativo.Schedulers.AbstractSchedule import AbstractSchedule


class SchedulerSJF(AbstractSchedule):

    def add(self,pcb):
        self._readyQueue.queue.append(pcb)
        self._readyQueue.queue.sort(key=lambda p: p.cantidadTotalDeProcesos)

    def isToExpropriate(self, pcbInPC, pcbNew):
        return pcbInPC.cantidadTotalDeProcesos > pcbNew.cantidadTotalDeProcesos

