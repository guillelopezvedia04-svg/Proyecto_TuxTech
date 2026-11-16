import sys

from PyQt6.QtWidgets import QApplication
from src.windows.login_window import Login

def main():
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()