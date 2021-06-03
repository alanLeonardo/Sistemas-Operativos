class PcbTable:

    def __init__(self):
        self._pcbs = []
        self._runningPcb = None
        self._count = 0

    @property
    def pcbs(self):
        return self._pcbs

    @property
    def runningPcb(self):
        return self._runningPcb

    def add(self, pcb):
        self._pcbs.append(pcb)

    def getNewPid(self):
        self._count = self._count + 1

        return self._count


