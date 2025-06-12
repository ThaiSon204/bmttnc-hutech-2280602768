from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# Tạo cặp khóa client từ tham số DH
def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

# Tính khóa chung từ private key client và public key server
def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    # Đọc khóa công khai từ server
    with open("server_public_key.pem", "rb") as f:
        server_public_key = serialization.load_pem_public_key(f.read())

    # Lấy tham số DH từ khóa công khai
    parameters = server_public_key.parameters()

    # Tạo khóa riêng và công khai phía client
    private_key, public_key = generate_client_key_pair(parameters)

    # Tính khóa bí mật chung (shared secret)
    shared_secret = derive_shared_secret(private_key, server_public_key)

    # In khóa chung ở dạng hex
    print("Shared Secret:", shared_secret.hex())

if __name__ == "__main__":
    main()