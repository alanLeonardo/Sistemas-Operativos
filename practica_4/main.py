from SistemaOperativo.Kernel.kernel import *
import log
from time import sleep

##
##  MAIN 
##
from SistemaOperativo.Program.Program import Program

if __name__ == '__main__':
    log.setupLogger()
    log.logger.info('Starting emulator')

    ## setup our hardware and set memory size to 25 "cells"
    HARDWARE.setup(25)

    ## Switch on computer
    HARDWARE.switchOn()

    ## new create the Operative System Kernel
    # "booteamos" el sistema operativo
    kernel = Kernel()

    prg1 = Program("prg1.exe", [ASM.CPU(2)])
    prg2 = Program("prg2.exe", [ASM.CPU(4)])
    prg3 = Program("prg3.exe", [ASM.CPU(3)])

    # execute all programs
    kernel.run(prg1,1)  ## 1 = prioridad del proceso
    kernel.run(prg2,3)  ## 2 = prioridad del proceso
    kernel.run(prg3,2)  ## 3 = prioridad del proceso





