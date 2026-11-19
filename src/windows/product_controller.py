from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QTableWidgetItem, QMessageBox


class ProductController:
    def __init__(
        self,
        tabla,
        nombre,
        descripcion,
        categoria,
        marca,
        proveedor,
        stock,
        precio,
        boton_guardar,
        service,
        categoria_service,
        marca_service,
        proveedor_service,
        modo="crear",
        boton_eliminar=None,
        al_cambiar=None,
        movement_service=None,
        id_usuario=None,
    ):
        self.tabla = tabla
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
        self.marca = marca
        self.proveedor = proveedor
        self.stock = stock
        self.precio = precio
        self.boton_guardar = boton_guardar
        self.service = service
        self.categoria_service = categoria_service
        self.marca_service = marca_service
        self.proveedor_service = proveedor_service
        self.modo = modo
        self.boton_eliminar = boton_eliminar
        self.al_cambiar = al_cambiar
        self.movement_service = movement_service
        self.id_usuario = id_usuario

        self.seleccionado_id = None
        self.fila_seleccionada = None
        self.filtro = ""

        self.configurar_tabla()
        self.boton_guardar.clicked.connect(self.guardar)

        if self.boton_eliminar is not None:
            self.boton_eliminar.clicked.connect(self.eliminar)

        if self.modo == "editar":
            self.tabla.currentCellChanged.connect(self.seleccionar)
            self.boton_guardar.setEnabled(False)

        self.cargar_combos()
        self.cargar()

    def configurar_tabla(self):
        self.tabla.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tabla.setColumnHidden(0, True)

        if self.modo == "editar":
            self.tabla.setSelectionBehavior(
                QAbstractItemView.SelectionBehavior.SelectRows
            )
            self.tabla.setSelectionMode(
                QAbstractItemView.SelectionMode.SingleSelection
            )
        else:
            self.tabla.setSelectionMode(
                QAbstractItemView.SelectionMode.NoSelection
            )

    def cargar_combos(self):
        self.cargar_combo(self.categoria, self.categoria_service)
        self.cargar_combo(self.marca, self.marca_service)
        self.cargar_combo(self.proveedor, self.proveedor_service)

    def cargar_combo(self, combo, service):
        seleccionado = combo.currentData()
        combo.clear()

        for registro in service.listar(include_inactive=False):
            combo.addItem(registro[1], registro[0])

        if seleccionado is not None:
            indice = combo.findData(seleccionado)
            if indice >= 0:
                combo.setCurrentIndex(indice)

    def cargar(self):
        registros = self.service.listar()

        self.tabla.blockSignals(True)
        self.tabla.setRowCount(0)

        for fila, registro in enumerate(registros):
            self.tabla.insertRow(fila)

            item_id = QTableWidgetItem(str(registro[0]))
            item_id.setData(
                Qt.ItemDataRole.UserRole,
                (registro[8], registro[9], registro[10]),
            )

            self.tabla.setItem(fila, 0, item_id)
            self.tabla.setItem(
                fila,
                1,
                QTableWidgetItem(registro[1]),
            )
            self.tabla.setItem(
                fila,
                2,
                QTableWidgetItem(registro[2] or ""),
            )
            self.tabla.setItem(
                fila,
                3,
                QTableWidgetItem(f"{float(registro[3]):.2f}"),
            )
            self.tabla.setItem(
                fila,
                4,
                QTableWidgetItem(str(registro[4])),
            )
            self.tabla.setItem(
                fila,
                5,
                QTableWidgetItem(registro[5]),
            )
            self.tabla.setItem(
                fila,
                6,
                QTableWidgetItem(registro[6]),
            )
            self.tabla.setItem(
                fila,
                7,
                QTableWidgetItem(registro[7]),
            )

        self.tabla.blockSignals(False)
        self.aplicar_filtro()

    def filtrar(self, texto):
        self.filtro = texto.strip().casefold()
        self.aplicar_filtro()

    def aplicar_filtro(self):
        for fila in range(self.tabla.rowCount()):
            item_nombre = self.tabla.item(fila, 1)
            nombre = item_nombre.text().casefold() if item_nombre else ""

            self.tabla.setRowHidden(fila, self.filtro not in nombre)

        if (
            self.fila_seleccionada is not None
            and self.tabla.isRowHidden(self.fila_seleccionada)
        ):
            self.limpiar()

    def seleccionar(self, fila, columna, fila_anterior, columna_anterior):
        if fila < 0:
            return

        item_id = self.tabla.item(fila, 0)
        if item_id is None:
            return

        self.seleccionado_id = int(item_id.text())
        self.fila_seleccionada = fila

        self.nombre.setText(self.tabla.item(fila, 1).text())

        descripcion = self.tabla.item(fila, 2)
        self.descripcion.setText(descripcion.text() if descripcion else "")

        self.precio.setValue(float(self.tabla.item(fila, 3).text()))
        self.stock.setValue(int(self.tabla.item(fila, 4).text()))

        ids = item_id.data(Qt.ItemDataRole.UserRole)
        if ids is not None:
            id_categoria, id_marca, id_proveedor = ids

            self.seleccionar_dato(
                self.categoria,
                id_categoria,
                self.tabla.item(fila, 5).text(),
            )
            self.seleccionar_dato(
                self.marca,
                id_marca,
                self.tabla.item(fila, 6).text(),
            )
            self.seleccionar_dato(
                self.proveedor,
                id_proveedor,
                self.tabla.item(fila, 7).text(),
            )

        self.boton_guardar.setEnabled(True)

        if self.boton_eliminar is not None:
            self.boton_eliminar.setEnabled(True)

    def seleccionar_dato(self, combo, valor, texto):
        indice = combo.findData(valor)

        if indice < 0 and valor is not None:
            combo.addItem(texto, valor)
            indice = combo.count() - 1

        if indice >= 0:
            combo.setCurrentIndex(indice)

    def limpiar(self):
        self.nombre.clear()
        self.descripcion.clear()
        self.stock.setValue(0)
        self.precio.setValue(0.0)

        for combo in (self.categoria, self.marca, self.proveedor):
            if combo.count() > 0:
                combo.setCurrentIndex(0)

        self.seleccionado_id = None
        self.fila_seleccionada = None
        self.tabla.clearSelection()

        if self.modo == "editar":
            self.boton_guardar.setEnabled(False)

        if self.boton_eliminar is not None:
            self.boton_eliminar.setEnabled(False)

    def guardar(self):
        if self.modo == "crear":
            self.agregar()
        else:
            self.actualizar()

    def agregar(self):
        stock_inicial = self.stock.value()

        success, message, id_producto = self.service.crear(
            self.nombre.text(),
            self.descripcion.text(),
            self.categoria.currentData(),
            self.marca.currentData(),
            self.proveedor.currentData(),
            stock_inicial,
            self.precio.value(),
        )

        if not success:
            QMessageBox.warning(self.tabla, "Productos", message)
            return

        self.registrar_movimiento(id_producto, 0, stock_inicial)
        QMessageBox.information(self.tabla, "Productos", message)
        self.limpiar()
        self.refrescar()

    def actualizar(self):
        if self.seleccionado_id is None:
            QMessageBox.warning(
                self.tabla,
                "Productos",
                "Selecciona un producto para actualizar.",
            )
            return

        stock_anterior = 0
        item_stock = self.tabla.item(self.fila_seleccionada, 4)
        if item_stock is not None:
            stock_anterior = int(item_stock.text())

        stock_nuevo = self.stock.value()

        success, message = self.service.actualizar(
            self.seleccionado_id,
            self.nombre.text(),
            self.descripcion.text(),
            self.categoria.currentData(),
            self.marca.currentData(),
            self.proveedor.currentData(),
            stock_nuevo,
            self.precio.value(),
        )

        if not success:
            QMessageBox.warning(self.tabla, "Productos", message)
            return

        self.registrar_movimiento(
            self.seleccionado_id,
            stock_anterior,
            stock_nuevo,
        )
        QMessageBox.information(self.tabla, "Productos", message)
        self.limpiar()
        self.refrescar()

    def eliminar(self):
        if self.seleccionado_id is None:
            QMessageBox.warning(
                self.tabla,
                "Productos",
                "Selecciona un producto para eliminar.",
            )
            return

        nombre = self.nombre.text().strip()

        if self.fila_seleccionada is not None:
            item_nombre = self.tabla.item(self.fila_seleccionada, 1)
            if item_nombre is not None:
                nombre = item_nombre.text()

        respuesta = QMessageBox.question(
            self.tabla,
            "Productos",
            f"¿Eliminar el producto '{nombre}'?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if respuesta != QMessageBox.StandardButton.Yes:
            return

        success, message = self.service.desactivar(self.seleccionado_id)

        if not success:
            QMessageBox.warning(self.tabla, "Productos", message)
            return

        QMessageBox.information(self.tabla, "Productos", message)
        self.limpiar()
        self.refrescar()

    def registrar_movimiento(self, id_producto, anterior, nueva):
        if self.movement_service is None:
            return

        if anterior == nueva:
            return

        self.movement_service.registrar(
            id_producto,
            self.id_usuario,
            anterior,
            nueva,
        )

    def refrescar(self):
        if self.al_cambiar is not None:
            self.al_cambiar()
        else:
            self.cargar()
