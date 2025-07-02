# Projeto Prático – Segurança da Informação

---

## Objetivo do Projeto

Desenvolver uma aplicação de troca de mensagens seguras em Python, utilizando os 3 pilares da segurança da informação:

- **Confidencialidade** com criptografia simétrica (AES no modo CBC)
- **Integridade e Autenticidade** com HMAC-SHA256
- **Autenticidade das chaves DH** usando assinaturas digitais com ECDSA

---

## 🛠️ Tecnologias e Bibliotecas Utilizadas

- `socket` – Comunicação TCP cliente-servidor
- `ecdsa` – Assinaturas digitais com curvas elípticas (ECDSA)
- `pycryptodome` – Criptografia AES
- `hashlib` + `hmac` – PBKDF2 e HMAC-SHA256
- `requests` – Para buscar a chave pública do outro lado (simulado via Gist)
- `json` – Para salvar e carregar as chaves derivadas

---

## 📁 Estrutura do Projeto
Projeto_Seguranca/
├── cliente_projeto.py # Realiza o handshake (DH + ECDSA) e deriva chaves
├── servidor_projeto.py # Recebe o handshake e deriva as chaves
├── cliente_envia_mensagem.py # Envia mensagem criptografada com AES e autenticada com HMAC
├── servidor_recebe_mensagem.py # Recebe a mensagem, valida HMAC e descriptografa
├── chaves_ECDSA/
│ ├── cliente.pem # Chave privada ECDSA do cliente
│ ├── servidor.pem # Chave privada ECDSA do servidor
├── chaves_cliente.json # Armazena Key_AES e Key_HMAC derivadas no cliente
├── chaves_servidor.json # Armazena Key_AES e Key_HMAC derivadas no servidor
├── requirements.txt # Dependências do projeto



---

## ⚙️ Passo a Passo para Execução

### 1. Clonar o projeto ou descompactar

```bash
cd ~/Downloads

2. Criar e ativar o ambiente virtual

Linux/macOS:

python3 -m venv venv
source venv/bin/activate

Windows (CMD):

python -m venv venv
venv\Scripts\activate

3. Instalar as dependências

pip install -r requirements.txt

Ou:

pip install ecdsa pycryptodome requests

4. Realizar o Handshake e derivação das chaves

Abra dois terminais:
Terminal 1 – Inicie o servidor:

python servidor_projeto.py

Terminal 2 – Execute o cliente:

python cliente_projeto.py

    Isso realiza:

        Troca de chaves Diffie-Hellman

        Assinatura/verificação com ECDSA

        Derivação das chaves AES e HMAC (via PBKDF2)

        Salvamento automático das chaves derivadas em arquivos .json

5. Enviar e receber a mensagem segura
Terminal 1 – Rode o receptor (servidor):

python servidor_recebe_mensagem.py

📤 Terminal 2 – Rode o cliente para enviar:

python cliente_envia_mensagem.py

    A mensagem é criptografada com AES-CBC, autenticada com HMAC-SHA256, e verificada com segurança no servidor.
