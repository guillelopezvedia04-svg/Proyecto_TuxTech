import sys

from PyQt6.QtWidgets import QApplication
from src.windows.login_window import Login
from src.database.connection import initialize_database

def main():
    initialize_database()
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()