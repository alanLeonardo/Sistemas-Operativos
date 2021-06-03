#!/usr/bin/env python
from tabulate import tabulate


class GanttDiagram:

    def __init__(self, kernel):
        self._kernel = kernel
        self._count = 1
        self._programas = [0]
        self._state = 0
        self._newPid = 0
        self._processes = [['Procesos', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],
                          [1, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "","","",""],
                          [2, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "","","",""],
                          [3, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "","","",""]]

    def updatePrograms(self, index):
        valor = self._programas[index]
        self._programas.pop(index)
        self._programas.insert(index, valor - 1)

    def tick(self, tickNbr):
        self.printPrograms(tickNbr)
        return print(tabulate(self._processes, headers='firstrow', tablefmt='fancy_grid'))

    def printPrograms(self, tickNbr):
        runningPcb = self._kernel.pcbTable.runningPcb
        p = self._count

        if runningPcb:
            pid = runningPcb.pid
            bursts = runningPcb._quantityBursts
            self.saveProcessQuantity(bursts, pid)
            self._newPid = pid
            self._processes[pid].pop(p)
            self._processes[pid].insert(p, self._programas[pid])
            self._count = p + 1
            self.updatePrograms(pid)

    def saveProcessQuantity(self, cant, pid):
        if self._state <= 1 and self._newPid != pid:
            self._programas.insert(pid, cant)
            self._state = cant - 1
        else:
            self._programas.insert(pid, self._state)
            self._state = self._state - 1

