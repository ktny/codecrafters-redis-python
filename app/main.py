import socket
import threading

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
                    store[key] = value
                    client_socket.send(bytes("+OK\r\n", "utf-8"))
                case "GET":
                    key = tokens[4]
                    response = store[key]
                    client_socket.send(bytes(f"${len(response)}\r\n{response}\r\n", "utf-8"))

        except ConnectionError:
            break


if __name__ == "__main__":
    main()
