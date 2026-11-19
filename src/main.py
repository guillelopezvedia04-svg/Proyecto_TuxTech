import sys

from PyQt6.QtWidgets import QApplication, QDialog

from src.windows.main_window import MainWindow
from src.windows.login_window import Login
from src.database.connection import initialize_database
from src.theme import aplicar_tema, tema_actual


def main():
    initialize_database()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    aplicar_tema(tema_actual())

    while True:
        login = Login()
        if login.exec() != QDialog.DialogCode.Accepted:
            break

        authenticated_user = login.authenticated_user
        window = MainWindow(authenticated_user)

        logout_requested = False

        def on_logout_requested():
            nonlocal logout_requested
            logout_requested = True

        window.logout_requested.connect(on_logout_requested)
        window.show()
        app.exec()

        if not logout_requested:
            break

    sys.exit(0)

if __name__ == "__main__":
    main()
