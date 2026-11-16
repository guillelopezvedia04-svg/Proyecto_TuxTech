-- Esquema de la base de datos de TuxTech
-- Contiene estructura, no datos reales.

PRAGMA foreign_keys = ON;

CREATE TABLE "categorias" (
	"idCategoria"	INTEGER,
	"nombreCategoria"	TEXT NOT NULL,
	PRIMARY KEY("idCategoria" AUTOINCREMENT)
);

CREATE TABLE "marca" (
	"idMarca"	INTEGER,
	"nombreMarca"	TEXT NOT NULL,
	PRIMARY KEY("idMarca" AUTOINCREMENT)
);

CREATE TABLE "movimientos" (
	"idMovimiento"	INTEGER,
	"idProducto"	INTEGER NOT NULL,
	"idUsuario"	INTEGER NOT NULL,
	"tipoMovimiento"	TEXT NOT NULL CHECK("tipoMovimiento" IN ('Venta', 'Compra', 'Ajuste', 'Eliminacion')),
	"cantidadAnterior"	INTEGER NOT NULL CHECK("cantidadAnterior" >= 0),
	"cantidadNueva"	INTEGER NOT NULL CHECK("cantidadNueva" >= 0),
	"fecha"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("idMovimiento" AUTOINCREMENT),
	FOREIGN KEY("idProducto") REFERENCES "productos"("idProducto"),
	FOREIGN KEY("idUsuario") REFERENCES "users"("idUser")
);

CREATE TABLE "productos" (
	"idProducto"	INTEGER,
	"idCategoria"	INTEGER NOT NULL,
	"idProveedor"	INTEGER NOT NULL,
	"idMarca"	INTEGER NOT NULL,
	"nombreProducto"	TEXT NOT NULL,
	"descripcion"	TEXT,
	"stock"	INTEGER NOT NULL CHECK("stock" >= 0),
	"precio"	INTEGER NOT NULL CHECK("precio" >= 0),
	"activo"	INTEGER NOT NULL DEFAULT 1 CHECK("activo" IN (0, 1)),
	PRIMARY KEY("idProducto" AUTOINCREMENT),
	FOREIGN KEY("idCategoria") REFERENCES "categorias"("idCategoria"),
	FOREIGN KEY("idMarca") REFERENCES "marca"("idMarca"),
	FOREIGN KEY("idProveedor") REFERENCES "proveedores"("idProveedor")
);

CREATE TABLE "proveedores" (
	"idProveedor"	INTEGER,
	"nombreProveedor"	TEXT NOT NULL,
	"contacto"	TEXT NOT NULL,
	PRIMARY KEY("idProveedor" AUTOINCREMENT)
);

CREATE TABLE "users" (
	"idUser"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"correo"	TEXT NOT NULL UNIQUE,
	PRIMARY KEY("idUser" AUTOINCREMENT)
);

