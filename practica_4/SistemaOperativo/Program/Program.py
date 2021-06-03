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

