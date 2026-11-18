from PyQt6.QtWidgets import QAbstractItemView, QTableWidgetItem, QMessageBox


class CatalogController:
    def __init__(
        self,
        tabla,
        nombre,
        descripcion,
        estado,
        boton_agregar,
        boton_actualizar,
        boton_estado,
        service,
    ):
        self.tabla = tabla
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado
        self.boton_agregar = boton_agregar
        self.boton_actualizar = boton_actualizar
        self.boton_estado = boton_estado
        self.service = service
        self.seleccionado_id = None
        self.seleccionado_activo = None

        self.configurar_tabla()
        self.boton_agregar.clicked.connect(self.agregar)
        self.boton_actualizar.clicked.connect(self.actualizar)
        self.boton_estado.clicked.connect(self.cambiar_estado)
        self.tabla.currentCellChanged.connect(self.seleccionar)
        self.cargar()

    def configurar_tabla(self):
        self.tabla.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabla.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabla.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tabla.setColumnHidden(0, True)
        self.boton_actualizar.setEnabled(False)
        self.boton_estado.setEnabled(False)

    def obtener_estado(self, combo):
        if combo.currentText() == "Activo":
            return 1
        return 0

    def cargar(self):
        registros = self.service.listar()

        self.tabla.blockSignals(True)
        self.tabla.setRowCount(0)

        for fila, registro in enumerate(registros):
            self.tabla.insertRow(fila)
            self.tabla.setItem(fila, 0, QTableWidgetItem(str(registro[0])))
            self.tabla.setItem(fila, 1, QTableWidgetItem(registro[1]))
            self.tabla.setItem(fila, 2, QTableWidgetItem(registro[2] or ""))
            estado = "Activo" if registro[3] else "Inactivo"
            self.tabla.setItem(fila, 3, QTableWidgetItem(estado))

        self.tabla.blockSignals(False)

    def seleccionar(self, fila, columna, fila_anterior, columna_anterior):
        if fila < 0:
            return

        item_id = self.tabla.item(fila, 0)
        if item_id is None:
            return

        self.seleccionado_id = int(item_id.text())
        self.nombre.setText(self.tabla.item(fila, 1).text())

        descripcion = self.tabla.item(fila, 2)
        self.descripcion.setText(descripcion.text() if descripcion else "")

        estado = self.tabla.item(fila, 3).text()
        self.estado.setCurrentIndex(0 if estado == "Activo" else 1)

        self.seleccionado_activo = estado == "Activo"
        self.boton_estado.setText(
            "Deshabilitar" if self.seleccionado_activo else "Habilitar"
        )

        self.boton_actualizar.setEnabled(True)
        self.boton_estado.setEnabled(True)

    def limpiar(self):
        self.nombre.clear()
        self.descripcion.clear()
        self.seleccionado_id = None
        self.seleccionado_activo = None
        self.boton_estado.setText("Deshabilitar")
        self.tabla.clearSelection()
        self.boton_actualizar.setEnabled(False)
        self.boton_estado.setEnabled(False)

    def agregar(self):
        nombre = self.nombre.text().strip()
        descripcion = self.descripcion.text().strip()
        activo = self.obtener_estado(self.estado)

        success, message = self.service.crear(
            nombre,
            descripcion,
            activo,
        )

        if not success:
            QMessageBox.warning(self.tabla, "Catálogos", message)
            return

        QMessageBox.information(self.tabla, "Catálogos", message)
        self.limpiar()
        self.cargar()

    def actualizar(self):
        if self.seleccionado_id is None:
            QMessageBox.warning(
                self.tabla,
                "Catálogos",
                "Selecciona una fila para actualizar.",
            )
            return

        success, message = self.service.actualizar(
            self.seleccionado_id,
            self.nombre.text(),
            self.descripcion.text(),
            self.obtener_estado(self.estado),
        )

        if not success:
            QMessageBox.warning(self.tabla, "Catálogos", message)
            return

        QMessageBox.information(self.tabla, "Catálogos", message)
        self.limpiar()
        self.cargar()

    def cambiar_estado(self):
        if self.seleccionado_id is None:
            QMessageBox.warning(
                self.tabla,
                "Catálogos",
                "Selecciona una fila para cambiar el estado.",
            )
            return

        nuevo_activo = 0 if self.seleccionado_activo else 1

        success, message = self.service.cambiar_estado(
            self.seleccionado_id,
            nuevo_activo,
        )

        if not success:
            QMessageBox.warning(self.tabla, "Catálogos", message)
            return

        QMessageBox.information(self.tabla, "Catálogos", message)
        self.limpiar()
        self.cargar()
