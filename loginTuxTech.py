import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit, QPushButton, QCheckBox

from loginTuxTech_ui import Ui_vtnLogin

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_vtnLogin()
        self.ui.setupUi(self)

        self.ui.chbVerPassword.toggled.connect(self.mostrar_password)


    def mostrar_password(self, mostrar: bool):
        if mostrar:
            self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)






if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())