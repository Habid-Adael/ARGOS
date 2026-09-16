from PySide6.QtCore import (
    QObject,
    Signal,
    QTimer
)


class PulseAnimation(QObject):

    pulse = Signal(float)

    def __init__(self):

        super().__init__()

        self.value = 0
        self.direction = 1


        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update
        )


    def start(self):

        self.timer.start(30)



    def update(self):

        self.value += 0.02 * self.direction


        if self.value >= 1:
            self.direction = -1


        if self.value <= 0:
            self.direction = 1


        self.pulse.emit(
            self.value
        )