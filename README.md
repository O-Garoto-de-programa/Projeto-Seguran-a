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

