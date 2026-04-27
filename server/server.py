import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

clients = []

# -----------------------------
# Send message to all clients
# -----------------------------
def broadcast(message, sender):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                clients.remove(client)

# -----------------------------
# Handle one client
# -----------------------------
def handle_client(client_socket, address):
    print(f"[CONNECTED] {address}")

    while True:
        try:
            # RECEIVE (decode incoming message)
            message = client_socket.recv(1024)

            if not message:
                break

            decoded = message.decode("utf-8")
            print(f"[{address}] {decoded}")

            # SEND (encode + broadcast)
            broadcast(message, client_socket)

        except:
            break

    print(f"[DISCONNECTED] {address}")
    clients.remove(client_socket)
    client_socket.close()

# -----------------------------
# Start server
# -----------------------------
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server.bind((HOST, PORT))
    server.listen()

    print(f"[STARTED] Server running on {HOST}:{PORT}")

    while True:
        client_socket, address = server.accept()

        clients.append(client_socket)

        thread = threading.Thread(
            target=handle_client,
            args=(client_socket, address)
        )
        thread.start()

        print(f"[ACTIVE CLIENTS] {len(clients)}")

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    start_server()