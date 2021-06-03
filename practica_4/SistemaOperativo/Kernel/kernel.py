#!/usr/bin/env python
from SistemaOperativo.Gantt.DescriptionByTick.DescriptionByTick import DescriptionByTick
from SistemaOperativo.Gantt.GanttDiagram.GanttDiagram import GanttDiagram
from SistemaOperativo.InterruptionHandler.IoInInterruptionHandler.IoInInterruptionHandler import IoInInterruptionHandler
from SistemaOperativo.InterruptionHandler.IoOutInterruptionHandler.IoOutInterruptionHandler import \
    IoOutInterruptionHandler
from SistemaOperativo.InterruptionHandler.KillInterruptionHandler.KillInterruptionHandler import KillInterruptionHandler
from SistemaOperativo.InterruptionHandler.NewInterruptionHandler.NewInterruptionHandler import NewInterruptionHandler
from SistemaOperativo.InterruptionHandler.TimerOutInterruptionHandler.TimerOutInterruptionHandler import \
    TimerOutInterruptionHandler
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

# emulates the core of an Operative System
class Kernel():

    def __init__(self):
        ## setup interruption handlers
        killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, killHandler)

        ioInHandler = IoInInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_IN_INTERRUPTION_TYPE, ioInHandler)

        ioOutHandler = IoOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(IO_OUT_INTERRUPTION_TYPE, ioOutHandler)

        newHandler = NewInterruptionHandler(self)
        HARDWARE.interruptVector.register(NEW_INTERRUPTION_TYPE, newHandler)

        timeoutHandler = TimerOutInterruptionHandler(self)
        HARDWARE.interruptVector.register(TIMEOUT_INTERRUPTION_TYPE, timeoutHandler)

        HARDWARE.clock.addSubscriber(DescriptionByTick(self))
        HARDWARE.clock.addSubscriber(GanttDiagram(self))

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)
        self._loader = Loader()

        self._pcbTable = PcbTable()
        self._dispatcher = Dispatcher(self)

        #self._schedule = SchedulerRoundRobin()
        #self._schedule.setQuantum(4)
        self._schedule = SchedulerPriorityExpropiativo()
        #self._schedule = SchedulerPriorityNoExpropiativo()
        #self._schedule = SchedulerFIFO()
        #self._schedule = SchedulerSJF()

    @property
    def ioDeviceController(self):
        return self._ioDeviceController

    @property
    def loader(self):
        return self._loader

    @property
    def pcbTable(self):
        return self._pcbTable

    @property
    def dispatcher(self):
        return self._dispatcher

    @property
    def scheduler(self):
        return self._schedule

    def setSchedule(self, schedule):
        self._schedule = schedule

    ## emulates a "system call" for programs execution

    def run(self, program, priority):
        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)
        tuple = (program, priority)
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, tuple)
        HARDWARE.interruptVector.handle(newIRQ)

    def __repr__(self):
        return "Kernel "
