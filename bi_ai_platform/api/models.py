from django.db import models
from .security import encrypt_text, decrypt_text

# Model para conexão com o banco de dados
class DatabaseConnection(models.Model):
    DB_TYPES = [
        ('postgres', 'PostgreSQL'),
        ('mysql', 'MySQL')
    ]


    name = models.CharField(max_length=200)
    db_type = models.CharField(max_length=10)
    host = models.CharField(max_length=200)
    port = models.IntegerField()
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=500)
    database = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        if not self.password.startswith('gAAAAA'):  # Evita criptografar duas vezes
            self.password = encrypt_text(self.password)
        super().save(*args, **kwargs)

    def get_decrypted_password(self):
        return decrypt_text(self.password)

    def __str__(self):
        return self.name
    

class TabelaSemantica(models.Model):
    nome_modelo_pbi = models.CharField(max_length=255, blank=True, null=True)  # Nome do modelo no Power BI (opcional)
    nome_tabela_modelo_pbi = models.CharField(max_length=255)  # Nome da tabela no modelo semântico
    nome_tabela_origem_db = models.CharField(max_length=255)  # Nome da tabela no banco de dados
    schema = models.CharField(max_length=255)
    banco = models.CharField(max_length=255)
    conexao = models.CharField(max_length=255)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_modelo_pbi
