from Hardware.hardware import *


class PageTable:
    def __init__(self, page, frame):
        self._page = page
        self._frame = frame

    @property
    def page(self):
        return self._page

    @property
    def frame(self):
        return self._frame
