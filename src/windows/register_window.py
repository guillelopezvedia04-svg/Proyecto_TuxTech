from PyQt6.QtWidgets import QDialog, QMessageBox, QLineEdit

from src.generated.registerTuxTech_ui import Ui_vtnRegister
from src.services.auth_service import register_user


class RegisterWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_vtnRegister()
        self.ui.setupUi(self)

        self.ui.txtPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.txtRepetirPassword.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.chbVerPassword.toggled.connect(self.mostrar_password)
        self.ui.btnRegistrar.clicked.connect(self.registrar_usuario)

    def mostrar_password(self, mostrar: bool):
        echo_mode = (
            QLineEdit.EchoMode.Normal
            if mostrar
            else QLineEdit.EchoMode.Password
        )
        self.ui.txtPassword.setEchoMode(echo_mode)
        self.ui.txtRepetirPassword.setEchoMode(echo_mode)

    def registrar_usuario(self):
        username = self.ui.txtUser.text()
        correo = self.ui.txtCorreo.text()
        password = self.ui.txtPassword.text()
        repetir_password = self.ui.txtRepetirPassword.text()

        if password != repetir_password:
            QMessageBox.warning(
                self,
                "Registro",
                "Las contraseñas no coinciden.",
            )
            return

        success, message = register_user(username, correo, password)

        if not success:
            QMessageBox.warning(self, "Registro", message)
            return

        QMessageBox.information(self, "Registro", message)
        self.accept()




