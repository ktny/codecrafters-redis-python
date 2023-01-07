import socket
import threading
from time import time

store = {}


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_socket, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_connection, args=(client_socket,)).start()


def handle_connection(client_socket: socket.socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break

            tokens = message.decode().split("\r\n")

            match tokens[2].upper():
                case "PING":
                    client_socket.send(bytes("+PONG\r\n", "utf-8"))
                case "ECHO":
                    client_socket.send(bytes(f"+{tokens[4]}", "utf-8"))
                case "SET":
                    key = tokens[4]
                    value = tokens[6]
                    expiry = None

                    # set expirty if exists PX
                    if len(tokens) > 8:
                        expiry = int(tokens[10]) + int(time() * 1000)

                    store[key] = (value, expiry)
                    client_socket.send(bytes("+OK\r\n", "utf-8"))
                case "GET":
                    key = tokens[4]
                    value, expiry = store[key]

                    if expiry is None or time() * 1000 < expiry:
                        client_socket.send(bytes(f"${len(value)}\r\n{value}\r\n", "utf-8"))
                    else:
                        client_socket.send(bytes("$-1\r\n", "utf-8"))

        except ConnectionError:
            break


if __name__ == "__main__":
    main()
