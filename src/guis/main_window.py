from PyQt6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Exemple PyQt")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Bonjour, PyQt !", self)
        self.label.setGeometry(50, 50, 300, 100)
