from pathlib import Path

from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QApplication


RAIZ = Path(__file__).resolve().parent.parent
ESTILOS = {
    True: RAIZ / "resources" / "styles" / "app_oscuro.qss",
    False: RAIZ / "resources" / "styles" / "app_claro.qss",
}


def tema_actual():
    settings = QSettings("TuxTech", "TuxTech")
    return settings.value("modo_oscuro", True, type=bool)


def guardar_tema(modo_oscuro: bool):
    settings = QSettings("TuxTech", "TuxTech")
    settings.setValue("modo_oscuro", modo_oscuro)
    settings.sync()


def aplicar_tema(modo_oscuro: bool):
    app = QApplication.instance()
    if app is None:
        return

    ruta = ESTILOS[modo_oscuro]
    app.setStyleSheet(ruta.read_text(encoding="utf-8"))
