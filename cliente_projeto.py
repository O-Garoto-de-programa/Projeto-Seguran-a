import socket
import hashlib
import os
from ecdsa import SigningKey, VerifyingKey
import json
import time
import requests
from hashlib import pbkdf2_hmac


g = 5
p = 115792089237316195423570985008687907853269984665640564039457584007913129640233

username_cliente = "ClientSeguranca2025"

with open("./chaves_ECDSA/cliente.pem", "rb") as f:
    sk_client = SigningKey.from_pem(f.read())

url = "https://gist.githubusercontent.com/ServerSeguranca2025/32a5c42318b9f1611d31a8c51caa75c3/raw/090b5fb6fa3e42e3a9e1165a496b08d688d4169e/server_public.pem"
response = requests.get(url)
chave_publica_servidor = response.content

try:
    vk = VerifyingKey.from_pem(chave_publica_servidor)
except Exception as e:
    print(f"Erro ao carregar a chave pública ECDSA do servidor: {e}")
    exit(1)

def gerar_chaves_DH(p, g):
    a_bytes = os.urandom(32)
    a = int.from_bytes(a_bytes, 'big')
    A = pow(g, a, p)
    return a, A

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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8080))

    print("Gerando Chaves a, A do Diffie-Hellman...")
    a, A = gerar_chaves_DH(p, g)
    time.sleep(1)
    print(f"Chave Pública A: {A}\n")

    print("Assinando a mensagem pra enviar para o Servidor...")
    mensagem = f"{A} {username_cliente}"
    sig_A = gerar_assinatura_ecdsa(sk_client, mensagem)
    mensagem_assinada_cliente = {
        "A": A,
        "assinatura_A": sig_A.hex(),
        "username_cliente": username_cliente
    }

    client_socket.send(json.dumps(mensagem_assinada_cliente).encode())
    print("MENSAGEM ASSINADA ENVIADA PARA O SERVIDOR!!!\n")
    print("___________________________________________________\n")
    print("ESPERANDO RESPOSTA DO SERVIDOR...\n")
    print("___________________________________________________\n")

    data = client_socket.recv(1024)
    mensagem_assinada_servidor = json.loads(data.decode())
    print("MENSAGEM RECEBIDA DO SERVIDOR!!!")

    B = int(mensagem_assinada_servidor["B"])
    sig_B = bytes.fromhex(mensagem_assinada_servidor["assinatura_B"])
    username_servidor = mensagem_assinada_servidor["username_servidor"]
    print(f"  B: {B}")
    print(f"  Assinatura Servidor: {sig_B}")
    print(f"  Username Servidor: {username_servidor}\n")
    time.sleep(1)

    print(f"VERIFICANDO ASSINATURA ECDSA DO SERVIDOR: {username_servidor}...")
    if not verificar_assinatura_ecdsa(vk, f"{B} {username_servidor}".encode(), sig_B):
        client_socket.close()
        print(f"\nConexão fechada com o servidor.")
        return
    S = pow(B, a, p)
    print("___________________________________________________\n")
    print(f"Chave Secreta compartilhada S: {S}\n")

    S_bytes = str(S).encode()
    salt = b'segurancaMichel2025'
    iterations = 100_000
    key_material = pbkdf2_hmac('sha256', S_bytes, salt, iterations, dklen=32)
    key_aes = key_material[:16]
    key_hmac = key_material[16:]

    print(f"Key_AES derivada (cliente): {key_aes.hex()}")
    print(f"Key_HMAC derivada (cliente): {key_hmac.hex()}")

    with open("chaves_cliente.json", "w") as f:
        json.dump({
            "key_aes": key_aes.hex(),
            "key_hmac": key_hmac.hex()
        }, f)

    print("Chaves salvas em chaves_cliente.json")

    print("___________________________________________________\n")

    client_socket.close()
    print("Conexão fechada com o servidor.")
    
if __name__ == "__main__":
    main()
