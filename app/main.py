import socket
import threading
from time import time
from typing import List

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
            response = process_tokens(tokens)
            client_socket.send(bytes(response, "utf-8"))
        except ConnectionError:
            break


def process_tokens(tokens: List[str]) -> str:
    command = tokens[2].upper()

    match command:
        case "PING":
            return "+PONG\r\n"
        case "ECHO":
            return f"+{tokens[4]}\r\n"
        case "SET":
            key = tokens[4]
            value = tokens[6]
            expiry = None

            # set expirty if exists PX
            if len(tokens) > 8:
                expiry = int(tokens[10]) + int(time() * 1000)

            store[key] = (value, expiry)
            return "+OK\r\n"
        case "GET":
            key = tokens[4]
            value, expiry = store[key]

            if expiry is None or time() * 1000 < expiry:
                return f"${len(value)}\r\n{value}\r\n"
            else:
                return "$-1\r\n"

    raise ValueError("Unknown Command")


if __name__ == "__main__":
    main()
