#!/usr/bin/env python
from SistemaOperativo.Dispacher import Dispatcher
from SistemaOperativo.DescriptionByTick import DescriptionByTick
from SistemaOperativo.InterruptionHandlers.IoInInterruptionHandler import IoInInterruptionHandler
from SistemaOperativo.InterruptionHandlers.IoOutInterruptionHandler import \
    IoOutInterruptionHandler
from SistemaOperativo.InterruptionHandlers.KillInterruptionHandler import KillInterruptionHandler
from SistemaOperativo.InterruptionHandlers.NewInterruptionHandler import NewInterruptionHandler
from SistemaOperativo.InterruptionHandlers.TimerOutInterruptionHandler import \
    TimerOutInterruptionHandler
from SistemaOperativo.IoDivice import *
from SistemaOperativo.Loader import *
from SistemaOperativo.MemoryManager import MemoryManager
from SistemaOperativo.PCBTable import *
from SistemaOperativo.FileSystem import *
from Hardware.hardware import *
from SistemaOperativo.Schedulers.SchedulerFIFO import SchedulerFIFO

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
        #HARDWARE.clock.addSubscriber(GanttDiagram(self))

        HARDWARE.mmu.frameSize = 4

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)

        self._pcbTable = PcbTable()
        self._dispatcher = Dispatcher()
        self._memoryManager = MemoryManager(self, HARDWARE.memory.size, HARDWARE.mmu.frameSize)
        self._fileSystem = FileSystem()
        self._loader = Loader(self.fileSystem, self._memoryManager)

        # Schedulers
        # self._schedule = SchedulerRoundRobin()
        # self._schedule.setQuantum(4)
        # self._schedule = SchedulerPriorityExpropiativo()
        # self._schedule = SchedulerPriorityNoExpropiativo()
        self._schedule = SchedulerFIFO()
        # self._schedule = SchedulerSJF()

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

    @property
    def fileSystem(self):
        return self._fileSystem

    @property
    def memoryManager(self):
        return self._memoryManager

    def setSchedule(self, schedule):
        self._schedule = schedule

    ## emulates a "system call" for programs execution

    def run(self, path, priority):
        program = self.fileSystem.read(path)

        program._path = path
        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)

        tuple = (program, priority)
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, tuple)
        HARDWARE.interruptVector.handle(newIRQ)

    def __repr__(self):
        return "Kernel "
