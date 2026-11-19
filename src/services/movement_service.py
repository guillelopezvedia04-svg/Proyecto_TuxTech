import sqlite3

from src.database.connection import get_connection


class MovementService:
    def registrar(
        self,
        id_producto,
        id_usuario,
        cantidad_anterior,
        cantidad_nueva,
        tipo="Ajuste",
    ):
        consulta = """
            INSERT INTO movimientos (
                idProducto,
                idUsuario,
                tipoMovimiento,
                cantidadAnterior,
                cantidadNueva
            )
            VALUES (?, ?, ?, ?, ?)
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    consulta,
                    (
                        id_producto,
                        id_usuario,
                        tipo,
                        cantidad_anterior,
                        cantidad_nueva,
                    ),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            return False

        return True

    def listar(self):
        consulta = """
            SELECT
                m.idMovimiento,
                p.nombreProducto,
                u.username,
                m.tipoMovimiento,
                m.cantidadAnterior,
                m.cantidadNueva,
                m.fecha
            FROM movimientos m
            JOIN productos p ON p.idProducto = m.idProducto
            JOIN users u ON u.idUser = m.idUsuario
            ORDER BY m.fecha DESC, m.idMovimiento DESC
        """

        with get_connection() as connection:
            return connection.execute(consulta).fetchall()
