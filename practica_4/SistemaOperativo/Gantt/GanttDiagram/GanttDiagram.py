#!/usr/bin/env python
from SistemaOperativo.IoDivice.IoDivice import *
from SistemaOperativo.Loader.loader import *
from SistemaOperativo.PcbTable.PCBTable import *
from SistemaOperativo.Dispacher.dispacher import *
from Hardware.hardware import *
from SistemaOperativo.Schedule.SchedulerFIFO.SchedulerFIFO import SchedulerFIFO
from SistemaOperativo.Schedule.SchedulerPriorityExpropiativo.SchedulerPriorityExpropiativo import \
    SchedulerPriorityExpropiativo
from SistemaOperativo.Schedule.SchedulerPriorityNoExpropiativo.SchedulerPriorityNoExpropiativo import \
    SchedulerPriorityNoExpropiativo
from SistemaOperativo.Schedule.SchedulerRoundRobin.SchedulerRoundRobin import SchedulerRoundRobin
from SistemaOperativo.Schedule.SchedulerSJF.SchedulerSJF import SchedulerSJF
from tabulate import tabulate

import log

class GanttDiagram:

    def __init__(self, kernel):
        self._kernel = kernel
        self._count = 1
        self._programas = [0]
        self._state = 0
        self._newPid = 0
        self._processes = [['Procesos', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16],
                          [1, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                          [2, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""],
                          [3, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]]

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

