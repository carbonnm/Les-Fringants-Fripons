from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        self.setWindowTitle("CodersLegacy")
        self.setLayout(layout)

        self.setStyleSheet(open("./guis/style.qss", "r").read())

        # Title Label
        title = QLabel("Login Form with PyQt6")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

        # Username Label and Input
        user = QLabel("Username:")
        user.setProperty("class", "normal")
        layout.addWidget(user, 1, 0)
        self.input1 = QLineEdit()
        layout.addWidget(self.input1, 1, 1, 1, 2)

        # Password Label and Input
        pwd = QLabel("Password")
        pwd.setProperty("class", "normal")
        layout.addWidget(pwd, 2, 0)
        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.input2, 2, 1, 1, 2)

        # Register and Login Buttons
        button1 = QPushButton("Register")
        layout.addWidget(button1, 4, 1)

        button2 = QPushButton("Login")
        button2.clicked.connect(self.login)
        layout.addWidget(button2, 4, 2)

    def login(self):
        if self.input1.text() == "CodersLegacy" and self.input2.text() == "12345678":
            print("Username and password are correct")
        else:
            print("Invalid")
