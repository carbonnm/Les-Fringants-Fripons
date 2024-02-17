import sys
from PyQt6.QtWidgets import QApplication
from guis.login_window import LoginFrame

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_frame = LoginFrame()
    login_frame.showMaximized()
    sys.exit(app.exec())
