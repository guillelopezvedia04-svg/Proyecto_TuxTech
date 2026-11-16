import sys

from PyQt6.QtWidgets import QApplication, QMainWindow

import icon_resources_rc
from mainTuxTech_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Navegacion entre las paginas del stckWidget
        self.ui.btnAgregar_short.clicked.connect(self.mostrar_agregar)
        self.ui.btnAgregar_long.clicked.connect(self.mostrar_agregar)
        self.ui.btnEditar_short.clicked.connect(self.mostrar_editar)
        self.ui.btnEditar_long.clicked.connect(self.mostrar_editar)
        self.ui.btnHistorial_short.clicked.connect(self.mostrar_historial)
        self.ui.btnHistorial_long.clicked.connect(self.mostrar_historial)

        # Configuracion inicial de la ventana
        self.ui.wdgBarraOculta.hide()
        self.ui.stckWidget.setCurrentIndex(0)
        self.ui.btnAgregar_long.setChecked(True)

    def mostrar_agregar(self):
        self.ui.stckWidget.setCurrentIndex(0)

    def mostrar_editar(self):
        self.ui.stckWidget.setCurrentIndex(1)

    def mostrar_historial(self):
        self.ui.stckWidget.setCurrentIndex(2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
