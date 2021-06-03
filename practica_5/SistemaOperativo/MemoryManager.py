class MemoryManager:

    def __init__(self, kernel, memorysize, framesize):
        self._kernel = kernel
        self._pageTable = dict()
        self._frames = memorysize // framesize
        self.freeFrames = list(range(0, self._frames))

    @property
    def pageTable(self):
        return self._pageTable

    def getFreeFrames(self):
        return self.freeFrames

    def allocFrames(self, n):
        size = len(self.freeFrames)
        freeFrames = self.freeFrames[0:n]

        self.freeFrames = self.freeFrames[n:size]


        return freeFrames

    def putPageTable(self, pid, pagetable):
        self._pageTable[pid] = pagetable

    def getPageTable(self, pid):
        return self._pageTable.get(pid)

    def removePageTable(self, pid):
        pTable = self.pageTable.get(pid)
        framesToRemove = []
        for index, element in enumerate(pTable):
            framesToRemove.append(element.frame)

        self.putFreeFrames(framesToRemove)
        self.pageTable.pop(pid)

    def putFreeFrames(self, listframes):
        return self.freeFrames.append(listframes)
