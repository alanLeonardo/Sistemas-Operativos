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

class DescriptionByTick:

    def __init__(self, kernel):
        self._kernel = kernel

    def tick(self, tickNbr):
        pid = "-"
        path = "-"
        runningPcb = self._kernel.pcbTable.runningPcb
        if runningPcb:
            pid = runningPcb.pid
            path = runningPcb.path

        log.logger.info("\n  CPU process :{pid} [{path}]".format(path=path, pid=pid))

