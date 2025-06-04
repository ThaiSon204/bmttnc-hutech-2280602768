class PlayFairCipher:
    def __init__(self) -> None:
        pass
        
    

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.upper()
        plain_text = plain_text.replace("J", "I")
        encrypted_text = ""
        for i in range(0, len(plain_text), 2):
            pair = plain_text[i:i+2]
            if len(pair) == 1: # Xử lý nếu số lượng ký tự lẻ
                pair += "X"
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text
    
    
    def create_playfair_matrix(self, key):
        key = key.replace("J", "I").upper()  # Chuyển "J" thành "I" và thành chữ hoa
        key = ''.join(dict.fromkeys(key))  # Loại bỏ ký tự trùng lặp, giữ thứ tự
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = list(key)
        # Thêm các chữ cái còn lại từ bảng chữ cái
        for letter in alphabet:
            if letter not in matrix:
                matrix.append(letter)
                if len(matrix) == 25:
                    break
        # Tạo ma trận 5x5
        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix
    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        cipher_text = ''.join(c for c in cipher_text if c.isalpha())
        if len(cipher_text) % 2 != 0:
            raise ValueError("Cipher text must have an even number of letters")
        decrypted_text = ""

        for i in range(0, len(cipher_text), 2):
            pair = cipher_text[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5]
                decrypted_text += matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1]
                decrypted_text += matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2]
                decrypted_text += matrix[row2][col1]

        # Xử lý các ký tự 'X' dư thừa
        i = 0
        while i < len(decrypted_text) - 2:
            if decrypted_text[i] == decrypted_text[i+2] and decrypted_text[i+1] == 'X':
                decrypted_text = decrypted_text[:i+1] + decrypted_text[i+2:]
            else:
                i += 2

        if decrypted_text.endswith("X"):
            decrypted_text = decrypted_text[:-1]

        return decrypted_text