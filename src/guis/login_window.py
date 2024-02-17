from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QCheckBox


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setStyleSheet(open("./styles/style.qss", "r").read())

        # Create main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create widget container
        widget_container = QWidget()
        widget_layout = QGridLayout()
        widget_container.setLayout(widget_layout)
        main_layout.addWidget(widget_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # Title Label
        title = QLabel("Welcome to Our Platform")
        title.setProperty("class", "heading")
        widget_layout.addWidget(title, 0, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Username Label and Input
        user_label = QLabel("Username:")
        user_label.setProperty("class", "normal")
        widget_layout.addWidget(user_label, 1, 0)
        self.username_input = QLineEdit()
        widget_layout.addWidget(self.username_input, 1, 1)

        # Password Label and Input
        pwd_label = QLabel("Password:")
        pwd_label.setProperty("class", "normal")
        widget_layout.addWidget(pwd_label, 2, 0)
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        widget_layout.addWidget(self.password_input, 2, 1)

        #Checkbox to hide/show the password
        self.show_pwd_checkbox = QCheckBox("Show Password")
        self.show_pwd_checkbox.stateChanged.connect(self.toggle_pwd_visibility)
        widget_layout.addWidget(self.show_pwd_checkbox, 3, 1, 1, 2)


        # Login Button
        login_button = QPushButton("Login")
        login_button.setProperty("class", "action")
        login_button.clicked.connect(self.login)
        widget_layout.addWidget(login_button, 4, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)


    def login(self):
        # Perform login authentication here
        username = self.username_input.text()
        password = self.password_input.text()
        # Add your authentication logic here
        if username == "CodersLegacy" and password == "12345678":
            print("Login successful")
        else:
            print("Invalid username or password")
    
    def toggle_pwd_visibility(self) -> None:
        if self.show_pwd_checkbox.checkState() == Qt.CheckState.Checked:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
