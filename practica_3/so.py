 #!/usr/bin/env python
from enum import Enum

from hardware import *
import log
from Process import *


class Program():

    def __init__(self, name, instructions):
        self._name = name
        self._instructions = self.expand(instructions)

    @property
    def name(self):
        return self._name

    @property
    def instructions(self):
        return self._instructions

    def addInstr(self, instruction):
        self._instructions.append(instruction)

    def expand(self, instructions):
        expanded = []
        for i in instructions:
            if isinstance(i, list):
                ## is a list of instructions
                expanded.extend(i)
            else:
                ## a single instr (a String)
                expanded.append(i)

        ## now test if last instruction is EXIT
        ## if not... add an EXIT as final instruction
        last = expanded[-1]
        if not ASM.isEXIT(last):
            expanded.append(INSTRUCTION_EXIT)

        return expanded

    def __repr__(self):
        return "Program({name}, {instructions})".format(name=self._name, instructions=self._instructions)


## emulates an Input/Output device controller (driver)
class IoDeviceController():

    def __init__(self, device):
        self._device = device
        self._waiting_queue = []
        self._currentPCB = None

    def runOperation(self, pcb, instruction):
        pair = {'pcb': pcb, 'instruction': instruction}
        # append: adds the element at the end of the queue
        self._waiting_queue.append(pair)

        # try to send the instruction to hardware's device (if is idle)
        self.__load_from_waiting_queue_if_apply()


    def getFinishedPCB(self):
        finishedPCB = self._currentPCB
        self._currentPCB = None
        self.__load_from_waiting_queue_if_apply()
        return finishedPCB

    def __load_from_waiting_queue_if_apply(self):
        if (len(self._waiting_queue) > 0) and self._device.is_idle:
            ## pop(): extracts (deletes and return) the first element in queue
            pair = self._waiting_queue.pop(0)
            #print(pair)
            pcb = pair['pcb']
            instruction = pair['instruction']
            self._currentPCB = pcb
            self._device.execute(instruction)


    def __repr__(self):
        return "IoDeviceController for {deviceID} running: {currentPCB} waiting: {waiting_queue}".format(deviceID=self._device.deviceId, currentPCB=self._currentPCB, waiting_queue=self._waiting_queue)

## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pid = self.kernel.pcbTable.getNewPid()
        program = irq.parameters
        nameProgram = irq.parameters.name
        baseDir = self.kernel.loader.load_program(program)

        pcbNew = PCB(pid, Process.NEW, nameProgram, baseDir)
        log.logger.info(pcbNew.pid)

        self.kernel.pcbTable.add(pcbNew)

        if self.kernel.pcbTable._runningPcb:
            pcbNew.changeState(Process.READY)
            self.kernel.readyQueue.addQueue(pcbNew)
        else:
            pcbNew.changeState(Process.READY)
            self.kernel.pcbTable._runningPcb = pcbNew
            self.kernel.dispatcher.load(pcbNew)


class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        log.logger.info(" Program Finished ")
        pcbRunning = self.kernel.pcbTable._runningPcb

        pcbRunning.changeState(Process.TERMINATED)

        self.kernel.dispatcher.save(pcbRunning)

        self.kernel.pcbTable._runningPcb = None
        log.logger.info(pcbRunning.pid)

        if self.kernel.readyQueue.queue:
            nextPcb = self.kernel.readyQueue.getProgram()
            self.kernel.dispatcher.load(nextPcb)
            nextPcb.changeState(Process.RUNNING)
            self.kernel.pcbTable._runningPcb = nextPcb
            log.logger.info(nextPcb.pid)

class IoInInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        operation = irq.parameters
        self.kernel.pcbTable._runningPcb.changeState(Process.WAITING)

        pcb = self.kernel.pcbTable._runningPcb

        self.kernel.dispatcher.save(pcb)

        self.kernel.pcbTable._runningPcb = None
        self.kernel.ioDeviceController.runOperation(pcb, operation)

        log.logger.info(pcb.pid)

        if self.kernel.readyQueue.queue:
            nextPcb = self.kernel.readyQueue.getProgram()
            self.kernel.dispatcher.load(nextPcb)
            nextPcb.changeState(Process.RUNNING)
            self.kernel.pcbTable._runningPcb = nextPcb
            log.logger.info(nextPcb.pid)

class IoOutInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        pcb = self.kernel.ioDeviceController.getFinishedPCB()
        pcb.changeState(Process.READY)
        log.logger.info(pcb.pid)

        if self.kernel.pcbTable.runningPcb:
            pcbReady = self.kernel.pcbTable._runningPcb
            pcbReady.changeState(Process.READY)
            self.kernel.dispatcher.save(pcbReady)
            self.kernel.readyQueue.addQueue(pcbReady)
            self.kernel.pcbTable._runningPcb = None
            log.logger.info(pcbReady.pid)

        self.kernel.pcbTable._runningPcb = pcb
        self.kernel.dispatcher.load(pcb)


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

        ## controls the Hardware's I/O Device
        self._ioDeviceController = IoDeviceController(HARDWARE.ioDevice)
        self._loader = Loader()

        self._pcbTable = PcbTable()
        self._dispatcher = Dispatcher(self)
        self._readyQueue = ReadyQueue(self)

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
    def readyQueue(self):
        return self._readyQueue


    ## emulates a "system call" for programs execution

    def run( self,program):

        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)
        newIRQ = IRQ(NEW_INTERRUPTION_TYPE, program)
        HARDWARE.interruptVector.handle(newIRQ)

    def __repr__(self):
        return "Kernel "

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




class Loader():

    def __init__(self):
        self._nextDir= 0

    def load_program(self, program):
        # loads the program in main memory
        baseDir: int = self._nextDir
        for index in program.instructions:
            HARDWARE.memory.write(self._nextDir, index)
            self._nextDir+=1
        return baseDir



class Dispatcher:
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def load(self,pcb):
        HARDWARE.mmu._baseDir = pcb.baseDir
        HARDWARE.cpu._pc = pcb.pc

    def save(self, pcb):
        pcb.updatePC(HARDWARE.cpu.pc)
        HARDWARE.cpu.pc = -1


class PCB:

    def __init__(self,pid,state,path,baseDir):
      self._pid = pid
      self._state = state
      self._pc = 0
      self._path = path
      self._baseDir = baseDir

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

    def setPC(self,pc):
       self._pc = pc

    def changeState(self,state):
        self._state = state

    def updatePC(self, pc):
        self._pc = pc

class ReadyQueue:
    def __init__(self, kernel):
        self._kernel = kernel
        self._queue = []

    @property
    def kernel(self):
        return

    @property
    def queue(self):
        return self._queue

    def addQueue(self, pcb):
        self._queue.append(pcb)

    def getProgram(self):
        return self.queue.pop(0)