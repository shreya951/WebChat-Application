import socket
import threading

HOST = "0.0.0.0"
PORT = 5555

# Store all connected clients
connected_clients = []

# Store usernames
client_names = {}


def broadcast_message(message, sender_socket):

    # Loop through every connected client
    for client_socket in connected_clients:

        # Ensure not to send message back to sender
        if client_socket != sender_socket:

            try:
                client_socket.send(message)

            except:
                # Remove broken client connection
                connected_clients.remove(client_socket)


def handle_client(client_socket, client_address):

    print(f"\n[NEW CONNECTION] {client_address}")

    try:
        # Get the first message from the client -> their username
        username = client_socket.recv(1024).decode("utf-8")

        # Save the username
        client_names[client_socket] = username

        print(f"[USERNAME] {client_address} is '{username}'")

        # Tell everyone the user joined
        join_message = f"\n[SERVER] {username} joined the chat!"
        broadcast_message(join_message.encode("utf-8"), client_socket)

    except:
        print("[ERROR] Could not get username")
        return

    # Keep listening for some messages
    while True:

        try:
            # Receive message from client
            message = client_socket.recv(1024)

            # If empty message, client disconnected
            if not message:
                break

            # Decode message into text
            decoded_message = message.decode("utf-8")

            print(f"[{username}] {decoded_message}")

            # Create message to send to others
            final_message = f"{username}: {decoded_message}"

            # Send message to all other clients
            broadcast_message(
                final_message.encode("utf-8"),
                client_socket
            )

        except:
            break


    print(f"[DISCONNECTED] {username}")

    connected_clients.remove(client_socket)

    leave_message = f"\n[SERVER] {username} left the chat."

    broadcast_message(
        leave_message.encode("utf-8"),
        client_socket
    )

    client_socket.close()


def start_server():

    # Create TCP socket
    server_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    # Bind socket to host + port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"[SERVER STARTED]")
    print(f"Listening on {HOST}:{PORT}\n")

    # Starts to accept new clients
    while True:

        # Accept new client
        client_socket, client_address = server_socket.accept()

        # Save client
        connected_clients.append(client_socket)

        print(f"[ACTIVE CLIENTS] {len(connected_clients)}")

        # Create the thread for this client
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address)
        )

        # Start the thread
        client_thread.start()

if __name__ == "__main__":
    start_server()