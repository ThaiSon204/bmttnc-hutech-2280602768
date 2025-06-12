from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair
server_key = RSA.generate(2048)

# List of connected clients
clients = []

# Function to encrypt message using AES
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)  # Sửa MODE_СВС thành MODE_CBC
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message using AES
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]  # Lấy IV đúng cách
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")

    # Gửi public key của server đến client
    client_socket.send(server_key.publickey().export_key(format='PEM'))

    # Nhận public key từ client
    client_received_key = RSA.import_key(client_socket.recv(2048))

    # Sinh AES key
    aes_key = get_random_bytes(16)

    # Mã hóa AES key bằng RSA public key của client
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)

    # Thêm client vào danh sách
    clients.append((client_socket, aes_key))

    try:
        while True:
            encrypted_message = client_socket.recv(2048)
            if not encrypted_message:
                break
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")

            # Gửi tin nhắn đã mã hóa tới các client khác
            for client, key in clients:
                if client != client_socket:
                    encrypted = encrypt_message(key, decrypted_message)
                    client.send(encrypted)

            if decrypted_message.strip().lower() == "exit":
                break
    except Exception as e:
        print(f"Error with {client_address}: {e}")
    finally:
        clients.remove((client_socket, aes_key))
        client_socket.close()
        print(f"Connection with {client_address} closed")

# Accept and handle client connections
def start_server():
    print("Server started and waiting for connections...")
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

start_server()
