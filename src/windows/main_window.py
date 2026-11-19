import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal

from src.generated import icon_resources_rc
from src.generated.mainTuxTech_ui import Ui_MainWindow
from src.services.catalog_service import CatalogService
from src.services.movement_service import MovementService
from src.services.product_service import ProductService
from src.windows.catalog_controller import CatalogController
from src.windows.history_controller import HistoryController
from src.windows.product_controller import ProductController


class MainWindow(QMainWindow):
    logout_requested = pyqtSignal()

    def __init__(self, authenticated_user):
        super().__init__()
        self.authenticated_user = authenticated_user
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.lblUser_2.setText(authenticated_user["username"])
        self.id_usuario = authenticated_user["idUser"]

        # Navegacion entre las paginas del stwPrincipal
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
        self.ui.stwPrincipal.setCurrentIndex(0)
        self.ui.stwCatalogo.setCurrentIndex(0)
        self.ui.btnAgregar_long.setChecked(True)
        self.ui.btnCategorias.setChecked(True)

        # Servicios
        self.categoria_servicio = CatalogService(
            nombreTabla="categorias",
            idColumna="idCategoria",
            nombreColumna="nombreCategoria",
        )
        self.marca_servicio = CatalogService(
            nombreTabla="marca",
            idColumna="idMarca",
            nombreColumna="nombreMarca",
        )
        self.proveedor_servicio = CatalogService(
            nombreTabla="proveedores",
            idColumna="idProveedor",
            nombreColumna="nombreProveedor",
        )
        self.producto_servicio = ProductService()
        self.movimiento_servicio = MovementService()

        # Controladores del catalogo
        self.categoria_controlador = CatalogController(
            tabla=self.ui.tbwCategoria,
            nombre=self.ui.txtNombrecategoria,
            descripcion=self.ui.txtDescripcionCategoria,
            estado=self.ui.cbxEstadoCategoria,
            boton_agregar=self.ui.btnAgregarCategoria,
            boton_actualizar=self.ui.btnActualizarCategoria,
            boton_estado=self.ui.btnDeshabilitaHabilitarCategoria,
            service=self.categoria_servicio,
        )
        self.marca_controlador = CatalogController(
            tabla=self.ui.tbwCategoriaMarca,
            nombre=self.ui.txtNombreMarca,
            descripcion=self.ui.txtDescripcionMarca,
            estado=self.ui.cbxEstadoMarca,
            boton_agregar=self.ui.btnAgregarMarca,
            boton_actualizar=self.ui.btnActualizarMarca,
            boton_estado=self.ui.btnDeshabilitaHabilitarMArca,
            service=self.marca_servicio,
        )
        self.proveedor_controlador = CatalogController(
            tabla=self.ui.tbwProveedores,
            nombre=self.ui.txtNombreProveedores,
            descripcion=self.ui.txtDescripcionProveedores,
            estado=self.ui.cbxProveedores,
            boton_agregar=self.ui.btnAgregarProveedores,
            boton_actualizar=self.ui.btnActualizarProveedores,
            boton_estado=self.ui.btnDeshabilitaHabilitarProveedores,
            service=self.proveedor_servicio,
        )

        # Controladores de productos
        self.producto_agregar_controlador = ProductController(
            tabla=self.ui.tbwAgregarProducto,
            nombre=self.ui.txtAgregarNombreProducto,
            descripcion=self.ui.txtAgregarDescripcionProducto,
            categoria=self.ui.cbxAgregarCategoriaProducto,
            marca=self.ui.cbxAgregarMarcaProducto,
            proveedor=self.ui.cbxAgregarProveedorProducto,
            stock=self.ui.sbAgregarStockProducto,
            precio=self.ui.sbAgregarPrecioProducto,
            boton_guardar=self.ui.btnAgregarProducto,
            service=self.producto_servicio,
            categoria_service=self.categoria_servicio,
            marca_service=self.marca_servicio,
            proveedor_service=self.proveedor_servicio,
            modo="crear",
            al_cambiar=self.refrescar_productos,
            movement_service=self.movimiento_servicio,
            id_usuario=self.id_usuario,
        )
        self.producto_editar_controlador = ProductController(
            tabla=self.ui.tbwActualizarProducto,
            nombre=self.ui.txtActualizarNombreProducto,
            descripcion=self.ui.txtActualizarDescripcionProducto,
            categoria=self.ui.cbxActualizarCategoriaProducto,
            marca=self.ui.cbxActualizarMarcaProducto,
            proveedor=self.ui.cbxActualizarProveedorProducto,
            stock=self.ui.sbActualizarStockProducto,
            precio=self.ui.sbActualizarPrecioProducto,
            boton_guardar=self.ui.btnActualizarProducto,
            service=self.producto_servicio,
            categoria_service=self.categoria_servicio,
            marca_service=self.marca_servicio,
            proveedor_service=self.proveedor_servicio,
            modo="editar",
            boton_eliminar=self.ui.btnEliminarProducto,
            al_cambiar=self.refrescar_productos,
            movement_service=self.movimiento_servicio,
            id_usuario=self.id_usuario,
        )

        self.historial_controlador = HistoryController(
            tabla=self.ui.tbwHistorial,
            service=self.movimiento_servicio,
        )

        # Busqueda universal
        self.ui.txtBuscar.textChanged.connect(self.buscar)
        self.actualizar_busqueda()

    def buscar(self, texto):
        controlador = self.controlador_actual()

        if controlador is not None:
            controlador.filtrar(texto)

    def controlador_actual(self):
        pagina = self.ui.stwPrincipal.currentIndex()

        if pagina == 0:
            return self.producto_agregar_controlador

        if pagina == 1:
            return {
                0: self.categoria_controlador,
                1: self.marca_controlador,
                2: self.proveedor_controlador,
            }[self.ui.stwCatalogo.currentIndex()]

        if pagina == 2:
            return self.producto_editar_controlador

        return None

    def actualizar_busqueda(self):
        pagina = self.ui.stwPrincipal.currentIndex()

        if pagina == 1:
            subpagina = self.ui.stwCatalogo.currentIndex()

            textos = {
                0: "Buscar en categorias...",
                1: "Buscar en marcas...",
                2: "Buscar en proveedores...",
            }
            botones = {
                0: self.ui.btnCategorias,
                1: self.ui.btnMarcas,
                2: self.ui.btnProveedores,
            }

            self.ui.txtBuscar.setPlaceholderText(
                textos.get(subpagina, "Buscar...")
            )
            botones[subpagina].setChecked(True)
        elif pagina == 2:
            self.ui.txtBuscar.setPlaceholderText("Buscar productos...")
        elif pagina == 3:
            self.ui.txtBuscar.setPlaceholderText("Buscar en historial...")
        else:
            self.ui.txtBuscar.setPlaceholderText("Buscar productos...")

        self.ui.txtBuscar.setEnabled(
            self.controlador_actual() is not None
        )
        self.ui.txtBuscar.clear()
        self.buscar("")

    def refrescar_productos(self):
        self.producto_agregar_controlador.cargar()
        self.producto_editar_controlador.cargar()

    def mostrar_agregar(self):
        self.ui.stwPrincipal.setCurrentIndex(0)
        self.producto_agregar_controlador.cargar_combos()
        self.actualizar_busqueda()

    def mostrar_editar(self):
        self.ui.stwPrincipal.setCurrentIndex(2)
        self.producto_editar_controlador.cargar_combos()
        self.actualizar_busqueda()

    def mostrar_historial(self):
        self.ui.stwPrincipal.setCurrentIndex(3)
        self.historial_controlador.cargar()
        self.actualizar_busqueda()

    def mostrar_catalogo(self):
        self.ui.stwPrincipal.setCurrentIndex(1)
        self.actualizar_busqueda()

    def mostrar_catalogo_categorias(self):
        self.ui.stwCatalogo.setCurrentIndex(0)
        self.actualizar_busqueda()

    def mostrar_catalogo_marcas(self):
        self.ui.stwCatalogo.setCurrentIndex(1)
        self.actualizar_busqueda()

    def mostrar_catalogo_proveedores(self):
        self.ui.stwCatalogo.setCurrentIndex(2)
        self.actualizar_busqueda()

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
