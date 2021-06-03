class PCB:

    def __init__(self,pid,state,path,baseDir,quantityBursts,priority):
      self._pid = pid
      self._state = state
      self._pc = 0
      self._path = path
      self._baseDir = baseDir
      self._quantityBursts = quantityBursts
      self._priority = priority

    @property
    def pid(self):
        return self._pid

    @property
    def baseDir(self):
        return self._baseDir

    @property
    def pc(self):
        return self._pc

    @property
    def state(self):
        return self._state

    @property
    def path(self):
        return self._path

    @property
    def quantityBursts(self):
        return self._quantityBursts

    @property
    def priority(self):
        return self._priority

    def setPC(self,pc):
       self._pc = pc

    def changeState(self,state):
        self._state = state

    def updatePC(self, pc):
        self._pc = pc