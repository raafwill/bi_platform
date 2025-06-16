from cryptography.fernet import Fernet
import base64
from django.conf import settings

# Gera uma chave de criptografia única (salvar no settings)
def generate_key():
    return base64.urlsafe_b64encode(Fernet.generate_key()).decode()

# Obtém a chave do settings
def get_cipher():
    key = settings.ENCRYPTION_KEY.encode()
    print(key)
    return Fernet(key)

# Função para criptografar texto
def encrypt_text(plain_text):
    cipher = get_cipher()
    return cipher.encrypt(plain_text.encode()).decode()

# Função para descriptografar texto
def decrypt_text(encrypted_text):
    cipher = get_cipher()
    return cipher.decrypt(encrypted_text.encode()).decode()
