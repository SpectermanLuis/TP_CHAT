#  PROGRAMACION SOBRE REDES
#  PRACTIFA FORMATIVA 1 
#  Alumno: Specterman Luis Omar
#  
#  Programa CLIENTE (envía mensajes a un servidor y los guarda en una base de datos SQLite.)


import socket


# Configuración del servidor al que se conectará el cliente
HOST = "localhost"
PUERTO = 5000


def conectar_servidor():
    """Crea el socket y se conecta al servidor."""

    # Configuración del socket TCP/IP
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Conexión con el servidor
        cliente.connect((HOST, PUERTO))

        print("Conectado al servidor.")
        print("Escribí tus mensajes.")
        print("Para terminar, escribí: éxito")

        return cliente

    except ConnectionRefusedError:
        print("No se pudo conectar con el servidor.")
        print("Verificá que el servidor esté ejecutándose.")

        return None


def enviar_mensajes(cliente):
    """Permite enviar varios mensajes al servidor."""

    while True:

        # Pedimos un mensaje al usuario
        mensaje = input("Mensaje: ")

        # Si el usuario escribe éxito, terminamos
        if mensaje.lower() == "éxito":
            print("Cliente finalizado.")
            break

        # Enviamos el mensaje al servidor
        cliente.send(mensaje.encode("utf-8"))

        # Esperamos la respuesta del servidor
        respuesta = cliente.recv(1024)

        # Mostramos la respuesta recibida
        print("Servidor:", respuesta.decode("utf-8"))


# Programa principal

cliente = conectar_servidor()

if cliente is not None:

    try:
        enviar_mensajes(cliente)

    finally:
        # Cerramos la conexión con el servidor
        cliente.close()
