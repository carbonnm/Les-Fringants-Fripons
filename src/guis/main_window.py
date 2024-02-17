from PyQt6.QtWidgets import QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window")

        self.button = QPushButton("Settings", self)
        self.button.clicked.connect(self.open_settings)
    
    def open_settings(self):
        settings_window = SettingsWindow()
        settings_window.exec_()
