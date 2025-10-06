import psycopg2
import getpass  # vuelve invisible en pantalla un input

# Configuración de conexión a la base de datos en Docker
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "credenciales"
DB_USER = "Admin"
DB_PASSWORD = "p4ssw0rdDB"


def conectar_db():
    """Conecta a la base de datos PostgreSQL y retorna la conexión."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn
    except Exception as e:
        print("Error de conexión:", e)
        return None


def obtener_datos_usuario(username, password):
    # Consulta la base de datos para obtener los datos de un usuario a partir de sus credenciales.
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Verificar si el usuario y contraseña existen en la tabla credenciales
        query = """
        SELECT u.id_usuario, u.nombre, u.correo, u.telefono, u.fecha_nacimiento
        FROM credenciales c
        JOIN usuarios u ON c.id_usuario = u.id_usuario
        WHERE c.username = %s AND c.password_hash = %s;
        """
        cursor.execute(query, (username, password))
        usuario = cursor.fetchone()

        if usuario:
            print("\nDatos del usuario encontrado:")
            print(f"ID: {usuario[0]}")
            print(f"Nombre: {usuario[1]}")
            print(f"Correo: {usuario[2]}")
            print(f"Teléfono: {usuario[3]}")
            print(f"Fecha de Nacimiento: {usuario[4]}")
            cursor.close()
            conn.close()
        else:
            print("\nUsuario o contraseña incorrectos.")
            cursor.close()
            conn.close()
    except Exception as e:
        print("Error al consultar la base de datos:", e)


def insertar_usuario(
    nombreNuevo, correoNuevo, telefonoNuevo, fechaNuevo, usuario, password
):
    conn = conectar_db()
    # si no logra conectarse no sigue
    if not conn:
        return

    try:
        cursor = conn.cursor()
        # Insertar nuevo usuario en la tabla usuarios
        cursor.execute(
            """
        INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento)
        VALUES (%s, %s, %s, %s) RETURNING id_usuario;
        """,
            (nombreNuevo, correoNuevo, telefonoNuevo, fechaNuevo),
        )
        # guardar el id del nuevo usuario
        id_usuario = cursor.fetchone()[0]

        # Insertar credenciales en la tabla credenciales
        cursor.execute(
            """
        INSERT INTO credenciales (id_usuario, username, password_hash)
        VALUES (%s, %s, %s);
        """,
            (id_usuario, usuario, password),
        )
        # Confirmar los cambios en la base de datos
        conn.commit()
        print("\nNuevo usuario insertado con éxito.")
    # Si hay error, no se hace el commit
    except Exception as e:
        print("Error al insertar el nuevo usuario:", e)
        # Revierte cualquier cambio si hay error
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

def actualizar_correo(id_usuario, nuevo_correo):
    conn = conectar_db()
    if not conn:
        return
    try:
        cursor = conn.cursor()
        # Actualizar el correo del usuario con el id proporcionado
        cursor.execute(
            """
        UPDATE usuarios
        SET correo = %s
        WHERE id_usuario = %s;
        """,
            (nuevo_correo, id_usuario),
        )
        # Confirmar los cambios en la base de datos
        conn.commit()
        if cursor.rowcount > 0:
            print("\nCorreo actualizado con éxito.")
        else:
            print("\nNo se encontró un usuario con el ID proporcionado.")
    except Exception as e:
        print("Error al actualizar el correo:", e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    #    print("Inicio de sesión en la base de datos")
    # Solicitar credenciales al usuario
    #    user = input("Ingrese su usuario: ")
    #    pwd = getpass.getpass("Ingrese su contraseña: ")#No muestra la contraseña a escribir
    #    #Consultar base de datos
    #    obtener_datos_usuario(user, pwd)
    #    print("insertar usuario")
    #nombreNuevo = input("ingrese nombre")
    #correoNuevo = input("ingrese correo")
    #telefonoNuevo = input("ingrese telefono")
    #fechaNuevo = input("ingrese fecha de nacimiento")
    #usuario = input("ingrese usuario")
    #password = getpass.getpass("ingrese contraseña")
    #insertar_usuario(nombreNuevo, correoNuevo, telefonoNuevo, fechaNuevo, usuario, password)
    print("Actualiza correo")
    id_usuario = input("ingrese id usuario a actualizar")
    nuevo_correo = input("ingrese nuevo correo")
    actualizar_correo(id_usuario, nuevo_correo) 