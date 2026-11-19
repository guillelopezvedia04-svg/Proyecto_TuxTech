import sqlite3

from src.database.connection import get_connection


class ProductService:
    def listar(self):
        consulta = """
            SELECT
                p.idProducto,
                p.nombreProducto,
                p.descripcion,
                p.precio,
                p.stock,
                c.nombreCategoria,
                m.nombreMarca,
                pr.nombreProveedor,
                p.idCategoria,
                p.idMarca,
                p.idProveedor,
                p.activo
            FROM productos p
            JOIN categorias c ON c.idCategoria = p.idCategoria
            JOIN marca m ON m.idMarca = p.idMarca
            JOIN proveedores pr ON pr.idProveedor = p.idProveedor
            WHERE p.activo = 1
            ORDER BY p.nombreProducto ASC
        """

        with get_connection() as connection:
            return connection.execute(consulta).fetchall()

    def crear(
        self,
        nombre,
        descripcion,
        id_categoria,
        id_marca,
        id_proveedor,
        stock,
        precio,
    ):
        error = self._validar(
            nombre,
            id_categoria,
            id_marca,
            id_proveedor,
            stock,
            precio,
        )

        if error:
            return False, error, None

        consulta = """
            INSERT INTO productos (
                idCategoria,
                idMarca,
                idProveedor,
                nombreProducto,
                descripcion,
                stock,
                precio,
                activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1)
        """

        try:
            with get_connection() as connection:
                cursor = connection.execute(
                    consulta,
                    (
                        id_categoria,
                        id_marca,
                        id_proveedor,
                        nombre.strip(),
                        descripcion.strip(),
                        stock,
                        precio,
                    ),
                )
                connection.commit()
                id_producto = cursor.lastrowid
        except sqlite3.IntegrityError:
            return (
                False,
                "No se pudo guardar el producto. Verifica los datos.",
                None,
            )

        return (
            True,
            "Producto agregado correctamente.",
            id_producto,
        )

    def actualizar(
        self,
        id_producto,
        nombre,
        descripcion,
        id_categoria,
        id_marca,
        id_proveedor,
        stock,
        precio,
    ):
        error = self._validar(
            nombre,
            id_categoria,
            id_marca,
            id_proveedor,
            stock,
            precio,
        )

        if error:
            return False, error

        consulta = """
            UPDATE productos
            SET idCategoria = ?,
                idMarca = ?,
                idProveedor = ?,
                nombreProducto = ?,
                descripcion = ?,
                stock = ?,
                precio = ?
            WHERE idProducto = ?
        """

        try:
            with get_connection() as connection:
                connection.execute(
                    consulta,
                    (
                        id_categoria,
                        id_marca,
                        id_proveedor,
                        nombre.strip(),
                        descripcion.strip(),
                        stock,
                        precio,
                        id_producto,
                    ),
                )
                connection.commit()
        except sqlite3.IntegrityError:
            return False, "No se pudo actualizar el producto. Verifica los datos."

        return True, "Producto actualizado correctamente."

    def desactivar(self, id_producto):
        consulta = """
            UPDATE productos
            SET activo = 0
            WHERE idProducto = ?
        """

        with get_connection() as connection:
            connection.execute(consulta, (id_producto,))
            connection.commit()

        return True, "Producto eliminado correctamente."

    def _validar(
        self,
        nombre,
        id_categoria,
        id_marca,
        id_proveedor,
        stock,
        precio,
    ):
        if not nombre or not nombre.strip():
            return "El nombre del producto no puede estar vacío."

        if (
            id_categoria is None
            or id_marca is None
            or id_proveedor is None
        ):
            return "Debes seleccionar categoría, marca y proveedor."

        if stock < 0:
            return "El stock no puede ser negativo."

        if precio < 0:
            return "El precio no puede ser negativo."

        return None
