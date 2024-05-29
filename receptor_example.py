import socket

# Configuración del socket
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 65432        # Puerto de comunicación

# Crear un socket TCP/IP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Conectado al servidor")

    while True:
        # Recibir datos del socket
        data = s.recv(1024)
        if not data:
            break

        # Convertir los datos a entero
        direccion = int(data.decode())
        print(f"Recibido dirección: {direccion}")