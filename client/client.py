import socket
import threading

HOST = "127.0.0.1"  # connect to your server (localhost)
PORT = 5555

# -----------------------------
# Receive messages from server
# -----------------------------
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            if not message:
                break
            print(message)
        except:
            print("[ERROR] Connection closed")
            client_socket.close()
            break

# -----------------------------
# Send messages to server
# -----------------------------
def send_messages(client_socket):
    while True:
        message = input()
        try:
            client_socket.send(message.encode("utf-8"))
        except:
            break

# -----------------------------
# Start client
# -----------------------------
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print("[CONNECTED TO SERVER]")
    except:
        print("[ERROR] Could not connect to server")
        return

    # Run receive + send in parallel
    threading.Thread(target=receive_messages, args=(client,)).start()
    threading.Thread(target=send_messages, args=(client,)).start()

if __name__ == "__main__":
    start_client()