from SistemaOperativo.InterruptionHandlers.AbstractInterruptionHandler import \
    AbstractInterruptionHandler
from SistemaOperativo.InterruptionHandlers.util.Process import Process

from SistemaOperativo.PCB import PCB


class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):

        pid = self.kernel.pcbTable.getNewPid()
        program = irq.parameters[0]
        pathProgram = program.path
        nameProgram = program.name
        cantidadTotalDeProcesos = len(program.instructions)
        priority = irq.parameters[1]
        pcbNew = PCB(pid, Process.NEW, pathProgram, cantidadTotalDeProcesos, priority, nameProgram)

        self.kernel.pcbTable.add(pcbNew)

        self.kernel.loader.load_program(pcbNew)




        if self.kernel.pcbTable._runningPcb:
            pcbINcpu = self.kernel.pcbTable.runningPcb
            self.expropriateOrSave(pcbINcpu, pcbNew)
        else:
            pcbNew.changeState(Process.RUNNING)
            self.kernel.pcbTable._runningPcb = pcbNew
            pageTable = self.kernel.memoryManager.getPageTable(pcbNew.pid)
            self.kernel.dispatcher.load(pcbNew,pageTable)

