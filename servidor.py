#  PROGRAMACION SOBRE REDES
#  PRACTIFA FORMATIVA 1 
#  Alumno: Specterman Luis Omar
#  
#  Programa SERVIDOR (recibe mensajes de un cliente y los guarda en una base de datos SQLite.)

import socket
import sqlite3
from datetime import datetime

# Configuración de la base de datos SQLite
NOMBRE_DB = "chat.db"

def inicializar_base_datos():
    """Crea la tabla mensajes si todavía no existe."""
    try:
        conexion = sqlite3.connect(NOMBRE_DB)

        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)

        conexion.commit()
        conexion.close()

        print("Base de datos inicializada correctamente.")

    except sqlite3.Error as error:
        print("Error al acceder a la base de datos:", error)
        return False

    return True


def inicializar_socket():
    """Crea y configura el socket TCP/IP del servidor."""

    # Configuración del socket TCP/IP
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar el puerto rápidamente después de cerrar el servidor
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # El servidor escuchará solamente en la computadora local
        servidor.bind(("localhost", 5000))

        # El servidor queda esperando conexiones
        servidor.listen()

        print("Servidor iniciado.")
        print("Escuchando en localhost:5000")

        return servidor

    except OSError as error:
        print("Error al iniciar el servidor.")
        print("Es posible que el puerto 5000 esté ocupado.")
        print("Detalle:", error)

        servidor.close()
        return None


def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    """Guarda un mensaje recibido en la base de datos."""

    try:
        conexion = sqlite3.connect(NOMBRE_DB)

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO mensajes
            (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """, (contenido, fecha_envio, ip_cliente))

        conexion.commit()
        conexion.close()

        return True

    except sqlite3.Error as error:
        print("Error al guardar el mensaje en la base de datos:", error)
        return False


def aceptar_conexion(servidor):
    """Acepta una conexión y recibe los mensajes del cliente."""

    print("Esperando conexión de un cliente...")

    try:
        conexion, direccion = servidor.accept()

        print("Cliente conectado:", direccion)

        while True:

            # Recibimos el mensaje enviado por el cliente
            datos = conexion.recv(1024)

            # Si no recibimos datos, el cliente cerró la conexión
            if not datos:
                break

            mensaje = datos.decode("utf-8")

            # Obtenemos la fecha y hora actual
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Dirección IP del cliente
            ip_cliente = direccion[0]

            # Guardamos el mensaje en la base de datos
            if guardar_mensaje(mensaje, timestamp, ip_cliente):

                # Respuesta que pide la consigna
                respuesta = "Mensaje recibido: " + timestamp

                conexion.send(respuesta.encode("utf-8"))

                print("Mensaje recibido:", mensaje)

            else:
                respuesta = "Error al guardar el mensaje"
                conexion.send(respuesta.encode("utf-8"))

        conexion.close()

        print("Cliente desconectado.")

    except OSError as error:
        print("Error en la comunicación con el cliente:", error)


# Programa principal

# Primero inicializamos la base de datos
if inicializar_base_datos():

    # Luego inicializamos el socket
    servidor = inicializar_socket()

    # Si el socket se pudo crear correctamente,
    # esperamos conexiones de clientes.
    if servidor is not None:

        try:
            while True:
                aceptar_conexion(servidor)

        except KeyboardInterrupt:
            print("\nServidor detenido por el usuario.")

        finally:
            servidor.close()