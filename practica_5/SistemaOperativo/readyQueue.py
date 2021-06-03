class ReadyQueue:
    def __init__(self):

        self._queue = []

    def __str__(self):
        return "%i - %s - %s" % (self.dorsal, self.nombre, self.demarcacion)

    @property
    def queue(self):
        return self._queue


    def addQueue(self, pcb):
        self._queue.append(pcb)