from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen
import math


class ArgosCore(QWidget):

    def __init__(self):

        super().__init__()

        self.energy = 0
        self.angle = 0
        self.state = "IDLE"
        self.wave_offset = 0

        self.setMinimumSize(320, 320)

        self.colors = {
            "IDLE": QColor(0, 180, 255),
            "LISTENING": QColor(0, 255, 255),
            "THINKING": QColor(180, 0, 255),
            "SPEAKING": QColor(0, 255, 120),
            "ERROR": QColor(255, 60, 60)
        }

        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)


    def animate(self):

        # Balanced animation speeds
        if self.state == "THINKING":
            self.angle += 1.2
            self.wave_offset += 1.5

        elif self.state == "LISTENING":
            self.angle += 0.6
            self.wave_offset += 1.4

        elif self.state == "SPEAKING":
            self.angle += 0.5
            self.wave_offset += 1.2

        else:  # IDLE
            self.angle += 0.5
            self.wave_offset += 1.0

        self.update()


    def set_state(self, state):

        self.state = state
        self.update()


    def update_energy(self, value):

        self.energy = value
        self.update()


    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        center = self.rect().center()
        color = self.colors.get(self.state, QColor(0, 180, 255))

        # -------------------------
        # IDLE animation
        # -------------------------
        if self.state == "IDLE":

            painter.save()
            painter.translate(center)
            painter.rotate(self.angle)

            pen = QPen(QColor(color.red(), color.green(), color.blue(), 100))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            painter.drawEllipse(-110, -110, 220, 220)

            painter.restore()

        # -------------------------
        # LISTENING animation
        # -------------------------
        elif self.state == "LISTENING":

            for i in range(3):

                radius = 75 + i * 22 + int(math.sin(self.wave_offset / 20) * 4)

                pen = QPen(QColor(color.red(), color.green(), color.blue(), 70 - i * 15))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.setBrush(Qt.NoBrush)

                painter.drawEllipse(center, radius, radius)

        # -------------------------
        # THINKING animation
        # -------------------------
        elif self.state == "THINKING":

            painter.save()
            painter.translate(center)

            painter.rotate(self.angle)

            pen = QPen(QColor(color.red(), color.green(), color.blue(), 150))
            pen.setWidth(3)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

            painter.drawEllipse(-115, -115, 230, 230)

            painter.rotate(-self.angle * 1.5)

            pen = QPen(QColor(color.red(), color.green(), color.blue(), 100))
            pen.setWidth(2)
            painter.setPen(pen)

            painter.drawEllipse(-80, -80, 160, 160)

            for i in range(4):

                angle = self.angle + i * 90

                x = 95 * math.cos(math.radians(angle))
                y = 95 * math.sin(math.radians(angle))

                painter.setBrush(QColor(color.red(), color.green(), color.blue(), 180))
                painter.setPen(Qt.NoPen)

                painter.drawEllipse(int(x) - 3, int(y) - 3, 6, 6)

            painter.restore()

        # -------------------------
        # SPEAKING animation
        # -------------------------
        elif self.state == "SPEAKING":

            for i in range(-3, 4):

                height = 35 + int(math.sin(self.wave_offset / 8 + i) * 8)

                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(color.red(), color.green(), color.blue(), 160))

                painter.drawRoundedRect(
                    center.x() + i * 20 - 5,
                    center.y() - height // 2,
                    10,
                    height,
                    5,
                    5
                )

        # -------------------------
        # Core glow
        # -------------------------

        glow_radius = 55 + int(math.sin(self.wave_offset / 25) * 3)

        for i in range(5, 0, -1):

            alpha = 15 * i

            painter.setBrush(QColor(color.red(), color.green(), color.blue(), alpha))
            painter.setPen(Qt.NoPen)

            painter.drawEllipse(center, glow_radius + i * 5, glow_radius + i * 5)

        # Core
        core_radius = 42 + int(math.sin(self.wave_offset / 20) * 2)

        painter.setBrush(QColor(color.red(), color.green(), color.blue(), 220))
        painter.setPen(Qt.NoPen)

        painter.drawEllipse(center, core_radius, core_radius)

        # Center eye
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(center, 7, 7)

        painter.end()