from flask import Flask, request, jsonify
from cipher.playfair.playfair_cipher import PlayFairCipher

app = Flask(__name__)

playfair_cipher = PlayFairCipher()

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_creatematrix():
    try:
        data = request.json
        if not data or 'key' not in data:
            return jsonify({'error': 'Missing key'}), 400
        key = data['key']
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        return jsonify({'playfair_matrix': playfair_matrix})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    try:
        data = request.json
        if not data or 'plain_text' not in data or 'key' not in data:
            return jsonify({'error': 'Missing plain_text or key'}), 400
        plain_text = data['plain_text']
        key = data['key']
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        encrypted_text = playfair_cipher.playfair_encrypt(plain_text, playfair_matrix)
        return jsonify({'encrypted_text': encrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    try:
        data = request.json
        if not data or 'cipher_text' not in data or 'key' not in data:
            return jsonify({'error': 'Missing cipher_text or key'}), 400
        cipher_text = data['cipher_text']
        key = data['key']
        playfair_matrix = playfair_cipher.create_playfair_matrix(key)
        decrypted_text = playfair_cipher.playfair_decrypt(cipher_text, playfair_matrix)
        return jsonify({'decrypted_text': decrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)