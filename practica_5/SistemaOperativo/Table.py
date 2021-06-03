#!/usr/bin/env python
from Hardware.hardware import *


class Table():

    def __init__(self,pid):
        self._pid = pid
        self._numerPageAndFrame = []

    @property
    def pid(self):
        return self._pid

    @property
    def numerPageAndFrame(self):
        return self._numerPageAndFrame

    def setPid(self, pid):
        self._pid = pid

    def setNumerPageAndNumerFrame(self, numerPage,numerFrame):
        self._numerPageAndFrame.append((numerPage,numerFrame))
