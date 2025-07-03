import socket
import hashlib
import hmac
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import json

with open("chaves_cliente.json", "r") as f:
    chaves = json.load(f)

key_aes = bytes.fromhex(chaves["key_aes"])
key_hmac = bytes.fromhex(chaves["key_hmac"])

mensagem_clara = "Segredo enviado com seguranca".encode('utf-8')
#imprir a mensagem clara
print(f"mensagem_clara: {mensagem_clara}")

iv = get_random_bytes(16)

padding_len = 16 - (len(mensagem_clara) % 16)
mensagem_padded = mensagem_clara + bytes([padding_len]) * padding_len

cipher = AES.new(key_aes, AES.MODE_CBC, iv)
mensagem_criptografada = cipher.encrypt(mensagem_padded)

# imprimir a mensagem criptografada
print(f"mensagem_criptografada: {mensagem_criptografada}")

conteudo = iv + mensagem_criptografada
tag_hmac = hmac.new(key_hmac, conteudo, hashlib.sha256).digest()

pacote = tag_hmac + conteudo

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1', 8081))
client_socket.send(pacote)
print("\nmensagem criptografada e autenticada enviada")
client_socket.close()