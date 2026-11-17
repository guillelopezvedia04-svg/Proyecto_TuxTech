import hashlib
import hmac
import secrets
import sqlite3

from src.database.connection import get_connection


HASH_ALGORITHM = "pbkdf2_sha256"
HASH_ITERATIONS = 310_000


def hash_password(password: str) -> str:
    """Genera un hash seguro para almacenar una contraseña."""
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        HASH_ITERATIONS,
    )

    return "$".join(
        (
            HASH_ALGORITHM,
            str(HASH_ITERATIONS),
            salt.hex(),
            password_hash.hex(),
        )
    )


def verify_password(password: str, stored_hash: str) -> bool:
    """Comprueba una contraseña contra un hash PBKDF2 almacenado."""
    try:
        algorithm, iterations, salt_hex, hash_hex = stored_hash.split("$", 3)
        if algorithm != HASH_ALGORITHM:
            return False

        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(hash_hex)
        actual_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )

        return hmac.compare_digest(actual_hash, expected_hash)
    except (ValueError, TypeError):
        return False


def authenticate_user(username: str, password: str):
    """Devuelve el usuario si las credenciales son válidas; si no, devuelve None."""
    username = username.strip()

    if not username or not password:
        return None

    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT idUser, username, password, correo
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    if user is None or not verify_password(password, user["password"]):
        return None

    return user


def register_user(username: str, correo: str, password: str) -> tuple[bool, str]:
    """Registra un usuario nuevo y devuelve el resultado de la operación."""
    username = username.strip()
    correo = correo.strip().lower()

    if not username or not correo or not password:
        return False, "Todos los campos son obligatorios."

    if "@" not in correo or "." not in correo.split("@")[-1]:
        return False, "Introduce un correo electrónico válido."

    try:
        with get_connection() as connection:
            if connection.execute(
                "SELECT 1 FROM users WHERE username = ?",
                (username,),
            ).fetchone() is not None:
                return False, "Ese nombre de usuario ya está registrado."

            if connection.execute(
                "SELECT 1 FROM users WHERE correo = ?",
                (correo,),
            ).fetchone() is not None:
                return False, "Ese correo electrónico ya está registrado."

            connection.execute(
                """
                INSERT INTO users (username, password, correo)
                VALUES (?, ?, ?)
                """,
                (username, hash_password(password), correo),
            )
            connection.commit()
    except sqlite3.IntegrityError:
        return False, "No se pudo registrar el usuario porque ya existe."

    return True, "Usuario registrado correctamente."
