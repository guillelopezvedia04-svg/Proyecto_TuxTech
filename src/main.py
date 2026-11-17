import sys

from PyQt6.QtWidgets import QApplication, QDialog

from src.windows.main_window import MainWindow
from src.windows.login_window import Login
from src.database.connection import initialize_database

def main():
    initialize_database()
    app = QApplication(sys.argv)

    login = Login()
    if login.exec() != QDialog.DialogCode.Accepted:
        return

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
