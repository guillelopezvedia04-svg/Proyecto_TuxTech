from PyQt6.QtWidgets import QAbstractItemView, QTableWidgetItem


class HistoryController:
    def __init__(self, tabla, service):
        self.tabla = tabla
        self.service = service

        self.configurar_tabla()
        self.cargar()

    def configurar_tabla(self):
        self.tabla.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.tabla.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tabla.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.tabla.setColumnHidden(0, True)

    def cargar(self):
        registros = self.service.listar()

        self.tabla.setRowCount(0)

        for fila, registro in enumerate(registros):
            self.tabla.insertRow(fila)
            self.tabla.setItem(
                fila,
                0,
                QTableWidgetItem(str(registro[0])),
            )
            self.tabla.setItem(
                fila,
                1,
                QTableWidgetItem(registro[1]),
            )
            self.tabla.setItem(
                fila,
                2,
                QTableWidgetItem(registro[2]),
            )
            self.tabla.setItem(
                fila,
                3,
                QTableWidgetItem(registro[3]),
            )
            self.tabla.setItem(
                fila,
                4,
                QTableWidgetItem(str(registro[4])),
            )
            self.tabla.setItem(
                fila,
                5,
                QTableWidgetItem(str(registro[5])),
            )
            self.tabla.setItem(
                fila,
                6,
                QTableWidgetItem(registro[6]),
            )
