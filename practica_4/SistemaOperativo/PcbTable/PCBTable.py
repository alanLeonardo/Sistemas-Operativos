class PcbTable:

    def __init__(self):
        self._pcbs = []
        self._runningPcb = None

    @property
    def pcbs(self):
        return self._pcbs

    @property
    def runningPcb(self):
        return self._runningPcb

    def add(self, pcb):
        self._pcbs.append(pcb)

    def getNewPid(self):
        return self.maxNumber()+1

    def maxNumber(self):
        return max(pcb.pid for pcb in self.pcbs) if self._pcbs else 0

