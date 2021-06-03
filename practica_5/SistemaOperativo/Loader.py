from SistemaOperativo.PageTable import PageTable
from SistemaOperativo.FileSystem import *


class Loader:

    def __init__(self,filesystem,memorymanager):
        self._fileSystem = filesystem
        self._logicalDirection = 0
        self._memoryManager = memorymanager

    @property
    def logicalDirection(self):
        return self.logicalDirection

    def load_program(self, pcb):
        #ir a buscar el programa en fileSystem
        program = self._fileSystem.read(pcb.path)
        #calcular los frame que puede ocupar el programa
        programFramesSize = self.calculateFrames(len(program.instructions)+1)
        #traigo los frames libres alocados en memory manager
        framesToAlloc = self.getAllocFrames(programFramesSize)



        self.createPageTable(pcb.pid, framesToAlloc)
        fz = self.getFrameSize()
        for index, frame in enumerate(framesToAlloc):
            #agrego a la memoria fisica las instrucciones
            #el primer frame va desde la direccion de instruccion 0 a 4
            #index= 0 fz=4
                self.putInstructions(program.instructions[index * fz: (index * fz) + fz], frame)


    def getAllocFrames(self, program_frames_size):
        return self._memoryManager.allocFrames(program_frames_size)

    def createPageTable(self, pid, frames_to_alloc):

        listPageTable = []
        for page, frame in enumerate(frames_to_alloc):
            listPageTable.append(PageTable(page, frame))

        self._memoryManager.putPageTable(pid, listPageTable)

    def calculateFrames(self, sizeProgram):
        #si el numero de instrucciones es impar, se agrega un frame mas
        framesAlloc = sizeProgram // self.getFrameSize()
        if sizeProgram % 2 != 0:
            framesAlloc = framesAlloc + 1

        return framesAlloc

    def putInstructions(self, instructions, frame):
        #primera direccion para escribir el programa en memoria que va de 0 a 4
        baseDir = frame * self.getFrameSize()
        for inst in instructions:
            HARDWARE.memory.write(baseDir + self._logicalDirection, inst)
            self._logicalDirection += 1
            #contador que se usa para desplazarse y escribir las instrucciones

        self._logicalDirection = 0

    def getFrameSize(self):
        return HARDWARE.mmu.frameSize


