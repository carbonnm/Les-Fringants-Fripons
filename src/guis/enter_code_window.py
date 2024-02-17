from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap, QIcon

class EnterCodeFrame(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Enter Code")
        self.setStyleSheet(open("./styles/style.qss", "r").read())
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        #Header "student profile"
        header = QLabel("Profil")
        header.setProperty("class", "heading")
        main_layout.addWidget(header, alignment = Qt.AlignmentFlag.AlignCenter)

        #Input of an evaluation code
        input_code = QLineEdit()
        input_code.setPlaceholderText("Enter code ...")
        main_layout.addWidget(input_code, alignment = Qt.AlignmentFlag.AlignCenter)

        #Validate button
        loupe = QPixmap("./img/loupe.png")
        loupe = loupe.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        search_button = QPushButton()
        search_button.setIcon(QIcon(loupe))
        search_button.setIconSize(loupe.size())  # Définir la taille de l'icône

        main_layout.addWidget(search_button, alignment=Qt.AlignmentFlag.AlignCenter)



    def validate_code(self):
        code = self.findChild(QLineEdit, "input_code").text()
        #Logique de quand on valide le code à rajouter ici

        print(code)
