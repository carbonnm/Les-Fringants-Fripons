import sys
from PyQt6.QtWidgets import QApplication
from guis.login_window import LoginWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.showMaximized()
    sys.exit(app.exec())