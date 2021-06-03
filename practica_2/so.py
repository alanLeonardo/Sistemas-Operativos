#!/usr/bin/env python

from hardware import *
import log
import queue
from collections import deque


## emulates a compiled program
from practica_2.hardware import INSTRUCTION_EXIT, KILL_INTERRUPTION_TYPE, HARDWARE, ASM


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


## emulates the  Interruptions Handlers
class AbstractInterruptionHandler():
    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def setKernel(self,kernel):
       self._kernel = kernel

    def execute(self, irq):
        log.logger.error("-- EXECUTE MUST BE OVERRIDEN in class {classname}".format(classname=self.__class__.__name__))

class KillInterruptionHandler(AbstractInterruptionHandler,):

    def __init__(self, state):
        self._state = True

    @property
    def state(self):
        return self._state

    def setStatePrograms(self,bool):
        self._state = bool

    def execute(self, irq):
        log.logger.info(" Program Finished ")
        # por ahora apagamos el hardware porque estamos ejecutando un solo programa

        if(self._state):
            Kernel.next(self.kernel)
        else:
            log.logger.info("Batch Finished")
            HARDWARE.switchOff()

# emulates the core of an Operative System
class Kernel():

    def __init__(self):
        ## setup interruption handlers
        self._killHandler = KillInterruptionHandler(self)
        HARDWARE.interruptVector.register(KILL_INTERRUPTION_TYPE, self._killHandler)
        self._q =queue.Queue(0)

    @property
    def q(self):
        return self._q

    @property
    def killHandler(self):
        return self._killHandler


    def load_program(self, program):
        # loads the program in main memory  
        progSize = len(program.instructions)
        for index in range(0, progSize):
            inst = program.instructions[index]
            HARDWARE.memory.write(index, inst)

    ## emulates a "system call" for programs execution  
    def run(self, program):
        self.load_program(program)
        log.logger.info("\n Executing program: {name}".format(name=program.name))
        log.logger.info(HARDWARE)

        # set CPU program counter at program's first intruction
        HARDWARE.cpu.pc = 0

    def listToQueu(self,batch):
        progSize = len(batch)
        for index in range(0, progSize):
            self._q.put(batch[index])


    def executeBatch(self, batch):
       self.listToQueu(batch)
       self._killHandler.setKernel(self)
       self.next()


    def next(self):
      self.run(self._q.get())
      self._killHandler.setStatePrograms(not self._q.empty())


    def __repr__(self):
        return "Kernel "
