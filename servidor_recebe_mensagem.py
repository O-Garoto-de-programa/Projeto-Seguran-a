import socket
import hashlib
import hmac
from Crypto.Cipher import AES
import json

with open("chaves_servidor.json", "r") as f:
    chaves = json.load(f)

key_aes = bytes.fromhex(chaves["key_aes"])
key_hmac = bytes.fromhex(chaves["key_hmac"])


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 8081))
server_socket.listen(1)
print("Servidor aguardando mensagem segura..")

client_socket, addr = server_socket.accept()
print(f"Conexao estabelecida com {addr}")

pacote = client_socket.recv(4096)

tag_recebido = pacote[:32]
iv = pacote[32:48]
mensagem_criptografada = pacote[48:]
conteudo = iv + mensagem_criptografada

tag_esperado = hmac.new(key_hmac, conteudo, hashlib.sha256).digest()

if not hmac.compare_digest(tag_recebido, tag_esperado):
    print("ERRO: HMAC invalido. Mensagem corrompida")
    client_socket.close()
    exit(1)

cipher = AES.new(key_aes, AES.MODE_CBC, iv)
mensagem_padded = cipher.decrypt(mensagem_criptografada)
padding_len = mensagem_padded[-1]
mensagem = mensagem_padded[:-padding_len]

print("Mensagem recebida com sucesso:")
print(mensagem.decode())

client_socket.close()
