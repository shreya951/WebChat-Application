import socket
import threading

# -----------------------------------
# SERVER CONNECTION SETTINGS
# -----------------------------------

HOST = "127.0.0.1"
PORT = 5555

# -----------------------------------
# RECEIVE MESSAGES FROM SERVER
# -----------------------------------

def receive_messages(client_socket):

    while True:

        try:
            # Receive message from server
            message = client_socket.recv(1024).decode("utf-8")

            # If empty message, connection closed
            if not message:
                break

            print("\n" + message)

        except:
            print("\n[DISCONNECTED FROM SERVER]")
            client_socket.close()
            break

# -----------------------------------
# SEND MESSAGES TO SERVER
# -----------------------------------

def send_messages(client_socket):

    while True:

        try:
            # Get message from keyboard
            message = input()

            # Send encoded message
            client_socket.send(message.encode("utf-8"))

        except:
            break

# -----------------------------------
# START CLIENT
# -----------------------------------

def start_client():

    # Create TCP socket
    client_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        # Connect to server
        client_socket.connect((HOST, PORT))

        print("[CONNECTED TO SERVER]")

    except:
        print("[ERROR] Could not connect")
        return

    # Ask user for username
    username = input("Enter your username: ")

    # Send username to server
    client_socket.send(username.encode("utf-8"))

    # Thread for receiving messages
    receive_thread = threading.Thread(
        target=receive_messages,
        args=(client_socket,)
    )

    # Thread for sending messages
    send_thread = threading.Thread(
        target=send_messages,
        args=(client_socket,)
    )

    # Start both threads
    receive_thread.start()
    send_thread.start()

# -----------------------------------
# RUN CLIENT
# -----------------------------------

if __name__ == "__main__":
    start_client()