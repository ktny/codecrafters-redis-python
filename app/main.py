import socket
import threading


def main():
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    while True:
        client_socket, _ = server_socket.accept()  # wait for client
        threading.Thread(target=handle_connection, args=(client_socket,)).start()


def handle_connection(client_connection: socket.socket):
    while True:
        try:
            client_connection.recv(1024)
            client_connection.send(b"+PONG\r\n")
        except ConnectionError:
            break


if __name__ == "__main__":
    main()
