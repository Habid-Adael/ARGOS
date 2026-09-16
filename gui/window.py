from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer

from gui.animations import PulseAnimation
from gui.core import ArgosCore

from assistant.status import get_status, status_manager


class ArgosWindow(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("A.R.G.O.S.")
        self.setFixedSize(450, 550)

        self.setStyleSheet("""
            QWidget {
                background-color: #050505;
                color: white;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.title = QLabel("""
A.R.G.O.S.

Autonomous Reasoning
and General Operating System
        """)

        self.title.setAlignment(Qt.AlignCenter)

        self.title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
            color:white;
        """)

        self.core = ArgosCore()

        self.status = QLabel()
        self.status.setAlignment(Qt.AlignCenter)

        self.status.setStyleSheet("""
            font-size:16px;
            color:#cccccc;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.core)
        layout.addWidget(self.status)

        self.setLayout(layout)

        # Animation
        self.animation = PulseAnimation()
        self.animation.pulse.connect(self.animate_core)
        self.animation.start()

        # Status updates
        status_manager.status_changed.connect(self.on_status_changed)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status)
        self.timer.start(500)


    def animate_core(self, value):

        self.core.update_energy(value)


    def on_status_changed(self, status):

        self.core.set_state(status)


    def update_status(self):

        self.status.setText(
            "SYSTEM STATUS:\n\n" + get_status()
        )


def start_gui():

    app = QApplication([])

    window = ArgosWindow()

    window.show()

    app.exec()