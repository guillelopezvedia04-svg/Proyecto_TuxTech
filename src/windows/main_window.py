import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal

from src.generated import icon_resources_rc
from src.generated.mainTuxTech_ui import Ui_MainWindow
from src.services.catalog_service import CatalogService
from src.windows.catalog_controller import CatalogController


class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self, authenticated_user):
        super().__init__()
        self.authenticated_user = authenticated_user
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lblUser_2.setText(authenticated_user["username"])

        # Navegacion entre las paginas del stckWidget
        self.ui.btnAgregar_short.clicked.connect(self.mostrar_agregar)
        self.ui.btnAgregar_long.clicked.connect(self.mostrar_agregar)
        self.ui.btnEditar_short.clicked.connect(self.mostrar_editar)
        self.ui.btnEditar_long.clicked.connect(self.mostrar_editar)
        self.ui.btnHistorial_short.clicked.connect(self.mostrar_historial)
        self.ui.btnHistorial_long.clicked.connect(self.mostrar_historial)
        self.ui.btnCatalogo_short.clicked.connect(self.mostrar_catalogo)
        self.ui.btnCatalogo_long.clicked.connect(self.mostrar_catalogo)

        self.ui.btnProveedores.clicked.connect(self.mostrar_catalogo_proveedores)
        self.ui.btnMarcas.clicked.connect(self.mostrar_catalogo_marcas)
        self.ui.btnCategorias.clicked.connect(self.mostrar_catalogo_categorias)

        self.ui.btnCerrarSesion_short.clicked.connect(self.cerrar_sesion)
        self.ui.btnCerrarSesion_long.clicked.connect(self.cerrar_sesion)

        # Configuracion inicial de la ventana
        self.ui.wdgBarraOculta.hide()
        self.ui.stckWidget.setCurrentIndex(0)
        self.ui.btnAgregar_long.setChecked(True)

        categoria_servicio = CatalogService(
            nombreTabla="categorias",
            idColumna="idCategoria",
            nombreColumna="nombreCategoria",
        )
        marca_servicio = CatalogService(
            nombreTabla="marca",
            idColumna="idMarca",
            nombreColumna="nombreMarca",
        )
        proveedor_servicio = CatalogService(
            nombreTabla="proveedores",
            idColumna="idProveedor",
            nombreColumna="nombreProveedor",
        )

        self.categoria_controlador = CatalogController(
            tabla=self.ui.tbwCategoria,
            nombre=self.ui.txtNombrecategoria,
            descripcion=self.ui.txtDescripcionCategoria,
            estado=self.ui.cbxEstadoCategoria,
            boton_agregar=self.ui.btnAgregarCategoria,
            boton_actualizar=self.ui.btnActualizarCategoria,
            boton_estado=self.ui.btnDeshabilitaHabilitarCategoria,
            service=categoria_servicio,
        )
        self.marca_controlador = CatalogController(
            tabla=self.ui.tbwCategoriaMarca,
            nombre=self.ui.txtNombreMarca,
            descripcion=self.ui.txtDescripcionMarca,
            estado=self.ui.cbxEstadoMarca,
            boton_agregar=self.ui.btnAgregarMarca,
            boton_actualizar=self.ui.btnActualizarMarca,
            boton_estado=self.ui.btnDeshabilitaHabilitarMArca,
            service=marca_servicio,
        )
        self.proveedor_controlador = CatalogController(
            tabla=self.ui.tbwProveedores,
            nombre=self.ui.txtNombreProveedores,
            descripcion=self.ui.txtDescripcionProveedores,
            estado=self.ui.cbxProveedores,
            boton_agregar=self.ui.btnAgregarProveedores,
            boton_actualizar=self.ui.btnActualizarProveedores,
            boton_estado=self.ui.btnDeshabilitaHabilitarProveedores,
            service=proveedor_servicio,
        )


    def mostrar_agregar(self):
        self.ui.stckWidget.setCurrentIndex(0)

    def mostrar_editar(self):
        self.ui.stckWidget.setCurrentIndex(2)

    def mostrar_historial(self):
        self.ui.stckWidget.setCurrentIndex(3)

    def mostrar_catalogo(self):
        self.ui.stckWidget.setCurrentIndex(1)


    def mostrar_catalogo_categorias(self):
        self.ui.stwCatalogo.setCurrentIndex(0)

    def mostrar_catalogo_marcas(self):
        self.ui.stwCatalogo.setCurrentIndex(1)

    def mostrar_catalogo_proveedores(self):
        self.ui.stwCatalogo.setCurrentIndex(2)

        

    def cerrar_sesion(self):
        self.authenticated_user = None
        self.logout_requested.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    usuario_prueba = {"idUser": 0, "username": "usuario"}
    window = MainWindow(usuario_prueba)
    window.show()
    sys.exit(app.exec())
