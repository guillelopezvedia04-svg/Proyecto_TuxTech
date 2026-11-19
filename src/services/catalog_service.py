import sqlite3

from src.database.connection import get_connection


class CatalogService:
    def __init__(self, nombreTabla, idColumna, nombreColumna):
        self.nombreTabla = nombreTabla
        self.idColumna = idColumna
        self.nombreColumna = nombreColumna

    def listar(self, include_inactive=True):
        filtro = "" if include_inactive else "WHERE activo = 1"

        consulta = f"""
            SELECT
                {self.idColumna},
                {self.nombreColumna},
                descripcion,
                activo
            FROM {self.nombreTabla}
            {filtro}
            ORDER BY {self.nombreColumna} ASC
        """

        with get_connection() as connection:
            return connection.execute(consulta).fetchall()

    def crear(self, nombre, descripcion="", activo=1):
        nombre = nombre.strip()
        descripcion = descripcion.strip()

        if not nombre:
            return False, "El nombre no puede estar vacío."

        if activo not in (0, 1):
            return False, "Estado no válido."

        consulta = f"""
            INSERT INTO {self.nombreTabla}
                ({self.nombreColumna}, descripcion, activo)
            VALUES (?, ?, ?)
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    consulta,
                    (nombre, descripcion, activo),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            return False, "Ya existe un registro con ese nombre."

        return True, "Registro creado exitosamente."

    def actualizar(self, id_registro, nombre, descripcion="", activo=1):
        nombre = nombre.strip()
        descripcion = descripcion.strip()

        if not nombre:
            return False, "El nombre no puede estar vacío."

        if activo not in (0, 1):
            return False, "Estado no válido."

        consulta = f"""
            UPDATE {self.nombreTabla}
            SET {self.nombreColumna} = ?,
                descripcion = ?,
                activo = ?
            WHERE {self.idColumna} = ?
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    consulta,
                    (nombre, descripcion, activo, id_registro),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            return False, "Ya existe un registro con ese nombre."

        return True, "Registro actualizado correctamente."

    def cambiar_estado(self, id_registro, activo):
        if activo not in (0, 1):
            return False, "Estado no válido."

        consulta = f"""
            UPDATE {self.nombreTabla}
            SET activo = ?
            WHERE {self.idColumna} = ?
        """

        with get_connection() as connection:
            connection.execute(
                consulta,
                (activo, id_registro),
            )
            connection.commit()

        return True, "Estado actualizado correctamente."
