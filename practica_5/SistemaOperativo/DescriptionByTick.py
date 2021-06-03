#!/usr/bin/env python

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

