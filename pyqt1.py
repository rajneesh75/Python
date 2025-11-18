from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
import sys


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel("Welcome, Rajneesh!", self)
        self.button = QPushButton("Click Me 👆", self)
        self.button.clicked.connect(self.on_click)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.setWindowTitle("PyQt Example")

    def on_click(self):
        self.label.setText("Button Clicked 🚀")


app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec_())
