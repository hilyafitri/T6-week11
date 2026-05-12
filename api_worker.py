"""
Nama  : Hilya Fitri
NIM   : F1D02310009
Kelas : C

"""

from PySide6.QtCore import QObject, Signal, QRunnable


class WorkerSignals(QObject):
    finished = Signal(object)
    error = Signal(str)


class ApiWorker(QRunnable):
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.signals = WorkerSignals()

    def run(self):
        try:
            result = self.function()
            self.signals.finished.emit(result)

        except Exception as e:
            self.signals.error.emit(str(e))