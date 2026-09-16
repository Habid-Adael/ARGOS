from PySide6.QtCore import QObject, Signal


class StatusManager(QObject):

    status_changed = Signal(str)

    def __init__(self):

        super().__init__()

        self.current_status = "IDLE"


    def set_status(self, status):

        self.current_status = status

        self.status_changed.emit(status)


    def get_status(self):

        return self.current_status


status_manager = StatusManager()


def set_status(status):

    status_manager.set_status(status)


def get_status():

    return status_manager.get_status()