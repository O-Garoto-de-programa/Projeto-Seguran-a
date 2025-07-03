import socket
from ecdsa import VerifyingKey, SigningKey
import hashlib
import os
import json
import time
import requests
from hashlib import pbkdf2_hmac

g = 5
p = 115792089237316195423570985008687907853269984665640564039457584007913129640233

username_server = "ServerSeguranca2025"

# Carrega a chave privada do servidor
with open("./chaves_ECDSA/servidor.pem", "rb") as f:
    sk_server = SigningKey.from_pem(f.read())

url = "https://gist.githubusercontent.com/ClientSeguranca2025/80c2087b9eb60d9c933c85d4d49c59e0/raw/f88a2a3ccb9482d3607e7379952eb51735f87517/cliente_public.pem"
response = requests.get(url)
chave_publica_cliente = response.content
vk = VerifyingKey.from_pem(chave_publica_cliente)

def gerar_chaves_DH(p, g):
    b_bytes = os.urandom(32)
    b = int.from_bytes(b_bytes, 'big')
    B = pow(g, b, p)
    return b, B

def gerar_assinatura_ecdsa(sk, mensagem):
    return sk.sign_deterministic(mensagem.encode(), hashfunc=hashlib.sha256)

def verificar_assinatura_ecdsa(vk, mensagem, assinatura):
    try:
        if vk.verify(assinatura, mensagem, hashfunc=hashlib.sha256):
            print("  OK - Verificação bem Sucedida\n")
            return True
    except Exception as e:
        print(f" ERRO - Falha na Verificação da mensagem: {e}\n")
    return False

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8080))
    server_socket.listen(1)
    print("Servidor aguardando conexão...")

    client_socket, addr = server_socket.accept()
    print(f"Conexao estabelecida com o cliente: {addr}\n")
    time.sleep(1)

    data = client_socket.recv(1024)
    mensagem_assinada_cliente = json.loads(data.decode())
    A = int(mensagem_assinada_cliente["A"])
    sig_A = bytes.fromhex(mensagem_assinada_cliente["assinatura_A"])
    username_cliente = mensagem_assinada_cliente["username_cliente"]

    print("MENSAGEM RECEBIDA DO CLIENTE")
    print(f"  A: {A}")
    print(f"  Assinatura Cliente: {sig_A}")
    print(f"  Username Cliente: {username_cliente}\n")

    print(f"VERIFICANDO ASSINATURA ECDSA DO CLIENTE: {username_cliente}...")
    if not verificar_assinatura_ecdsa(vk, f"{A} {username_cliente}".encode(), sig_A):
        client_socket.close()
        print("Conexão fechada com o cliente.")
        return

    b, B = gerar_chaves_DH(p, g)
    print(f"Chave Pública B: {B}\n")

    mensagem = f"{B} {username_server}"
    sig_B = gerar_assinatura_ecdsa(sk_server, mensagem)
    mensagem_assinada_servidor = {
        "B": B,
        "assinatura_B": sig_B.hex(),
        "username_servidor": username_server
    }
    client_socket.send(json.dumps(mensagem_assinada_servidor).encode())
    print("MENSAGEM ASSINADA ENVIADA PARA O CLIENTE!!!\n")

    S = pow(A, b, p)
    print("___________________________________________________\n")
    print(f"Chave Secreta compartilhada S: {S}\n")

    S_bytes = str(S).encode()
    salt = b'segurancaMichel2025'
    iterations = 100_000
    key_material = pbkdf2_hmac('sha256', S_bytes, salt, iterations, dklen=32)
    key_aes = key_material[:16]
    key_hmac = key_material[16:]

    print(f"Key_AES derivada (servidor): {key_aes.hex()}")
    print(f"Key_HMAC derivada (servidor): {key_hmac.hex()}")

    with open("chaves_servidor.json", "w") as f:
        json.dump({
            "key_aes": key_aes.hex(),
            "key_hmac": key_hmac.hex()
        }, f)

    print("Chaves salvas em chaves_servidor.json")

    print("___________________________________________________\n")

    client_socket.close()
    print("Conexão fechada com o cliente.")

if __name__ == "__main__":
    main()
