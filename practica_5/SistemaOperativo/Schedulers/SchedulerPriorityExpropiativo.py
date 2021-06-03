from SistemaOperativo.Schedulers.AbstractSchedule import AbstractSchedule


class SchedulerPriorityExpropiativo(AbstractSchedule):

    def add(self,pcb):
        self.readyQueue.addQueue(pcb)
        self.readyQueue.queue.sort(key=lambda p: p.priority)

    def isToExpropriate(self, pcbInPC, pcbNew):
        return pcbInPC.priority > pcbNew.priority
