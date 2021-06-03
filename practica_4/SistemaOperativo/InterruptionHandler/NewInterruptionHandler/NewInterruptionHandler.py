from SistemaOperativo.InterruptionHandler.AbstractInterruptionHandler.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.InterruptionHandler.util.Process import *
from SistemaOperativo.PCB.PCB import *


class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):

        pid = self.kernel.pcbTable.getNewPid()
        program = irq.parameters[0]
        nameProgram = program.name
        baseDir = self.kernel.loader.load_program(program)
        cantidadTotalDeProcesos = len(program.instructions)
        priority = irq.parameters[1]
        pcbNew = PCB(pid, Process.NEW, nameProgram, baseDir, cantidadTotalDeProcesos, priority)

        self.kernel.pcbTable.add(pcbNew)

        if self.kernel.pcbTable._runningPcb:
            pcbINcpu = self.kernel.pcbTable.runningPcb
            self.expropriateOrSave(pcbINcpu, pcbNew)
        else:
            pcbNew.changeState(Process.RUNNING)
            self.kernel.pcbTable._runningPcb = pcbNew
            self.kernel.dispatcher.load(pcbNew)

