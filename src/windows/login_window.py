import sys
from PyQt6.QtWidgets import QApplication, QDialog, QMessageBox, QLineEdit

from src.generated.loginTuxTech_ui import Ui_vtnLogin
from src.services.auth_service import authenticate_user
from src.windows.register_window import RegisterWindow

class Login(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_vtnLogin()
        self.ui.setupUi(self)

        self.ui.chbVerPassword.toggled.connect(self.mostrar_password)
        self.ui.btnEntrar.clicked.connect(self.iniciar_sesion)
        self.ui.btnRegistrar.clicked.connect(self.abrir_registro)


    def mostrar_password(self, mostrar: bool):
        if mostrar:
            self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def iniciar_sesion(self):
        username = self.ui.txtUser.text()
        password = self.ui.txtPassword.text()

        user = authenticate_user(username, password)

        if user is None:
            QMessageBox.warning(
                self,
                "Inicio de sesión",
                "El usuario o la contraseña no son válidos.",
            )
            return

        self.accept()

    def abrir_registro(self):
        registro = RegisterWindow(self)
        registro.exec()






if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())
