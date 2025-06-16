from django.shortcuts import render
from rest_framework import viewsets, generics, status
from .models import DatabaseConnection, TabelaSemantica
from .serializers import DatabaseConnectionSerializer, UserSerializer, TabelaSemanticaSerializer, PbitUploadSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from .database_utils import test_database_connection
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.db import connection
import psycopg2
import pymysql
import zipfile
import json
from rest_framework.views import APIView
import re

class DatabaseConnectionViewSet(viewsets.ModelViewSet):
    queryset = DatabaseConnection.objects.all()
    serializer_class = DatabaseConnectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Admin').exists():
            return DatabaseConnection.objects.all()
        return DatabaseConnection.objects.none()
    
class TestDatabaseConnectionView(generics.GenericAPIView):
    serializer_class = DatabaseConnectionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        db_entry = DatabaseConnection(
            db_type=data.get('db_type'),
            host=data.get('host'),
            port=data.get('port'),
            username=data.get('username'),
            password=data.get('password'),
            database=data.get('database')
        )
        decrypted_password = db_entry.get_decrypted_password()
        result = test_database_connection(
            db_entry.db_type, db_entry.host, db_entry.port,
            db_entry.username, decrypted_password, db_entry.database
        )
        return Response(result)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Criando Permissões Customizadas
def create_groups():
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    client_group, _ = Group.objects.get_or_create(name='Cliente')

    # Permissões para Admin
    admin_group.permissions.set([])

    # Permissões para Cliente (apenas leitura)
    client_group.permissions.set([])

# View para listar conexões
@api_view(['GET'])
def list_connections(request):
    connections = DatabaseConnection.objects.all()
    serializer = DatabaseConnectionSerializer(connections, many=True)
    return Response(serializer.data)

# View para criar conexões
@api_view(['POST'])
def create_connection(request):
    print("📥 Dados recebidos:", request.data)  # 👀 Log para depuração

    required_fields = ["name", "host", "port", "database", "user", "password"]
    missing_fields = [field for field in required_fields if field not in request.data]

    if missing_fields:
        return Response(
            {"error": f"Campos ausentes: {', '.join(missing_fields)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )


    serializer = DatabaseConnectionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# View para atualizar/editar conexões
@api_view(['PUT'])
def update_connection(request, pk):
    try:
        connection = DatabaseConnection.objects.get(pk=pk)
    except DatabaseConnection.DoesNotExist:
        return Response({'error': 'Conexão não encontrada'}, status=404)
    
    serializer = DatabaseConnectionSerializer(connection, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

# View para deletar conexões
@api_view(['DELETE'])
def delete_connection(request, pk):
    try:
        connection = DatabaseConnection.objects.get(pk=pk)
        connection.delete()
        return Response({'message': 'Conexão deletada com sucesso'}, status=204)
    except DatabaseConnection.DoesNotExist:
        return Response({'error': 'Conexão não encontrada'}, status=404)
    

@api_view(['POST'])
def test_connection(request):
    db_type = request.data.get("db_type")
    host = request.data.get("host")
    port = request.data.get("port")
    user = request.data.get("user")
    password = request.data.get("password")
    database = request.data.get("database")

    try:
        if db_type == "PostgreSQL":
            conn = psycopg2.connect(
                dbname=database, user=user, password=password, host=host, port=port
            )
        elif db_type == "MySQL":
            conn = pymysql.connect(
                host=host, user=user, password=password, database=database, port=int(port)
            )
        else:
            return Response({"error": "Tipo de banco não suportado"}, status=400)
        
        conn.close()
        return Response({"message": "Conexão bem-sucedida!"}, status=200)
    
    except Exception as e:
        return Response({"error": str(e)}, status=400)


@api_view(["GET"])
def list_table_data(request, table_name):
    """Retorna os dados de uma tabela específica"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 100")  # Evita sobrecarregar
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        data = [dict(zip(columns, row)) for row in rows]
        return JsonResponse({"table": table_name, "data": data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
    

@api_view(['GET', 'POST'])
def tabela_semantica_view(request):
    if request.method == 'POST':
        serializer = TabelaSemanticaSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        tabelas = TabelaSemantica.objects.all()
        serializer = TabelaSemanticaSerializer(tabelas, many=True)
        return Response(serializer.data)
    
class ImportarPbitView(APIView):
    def post(self, request):
        serializer = PbitUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        arquivo = serializer.validated_data['arquivo']
        try:
            with zipfile.ZipFile(arquivo) as zip_ref:
                with zip_ref.open("DataModelSchema") as schema_file:
                    schema = json.load(schema_file)

            nome_modelo_pbi = arquivo.name.replace(".pbit", "").replace(".pbix", "")

            tabelas = schema.get("model", {}).get("tables", [])
            registros_criados = 0

            for tabela in tabelas:
                nome_tabela_modelo_pbi = tabela.get("name", "sem_nome")
                partitions = tabela.get("partitions", [])
                if not partitions:
                    print(f"⛔ Tabela '{nome_tabela_modelo_pbi}' não possui 'partitions'.")
                    continue

                source = partitions[0].get("source")
                if not source:
                    print(f"⛔ Tabela '{nome_tabela_modelo_pbi}' não possui 'source'.")
                    continue

                expression = source.get("expression", [])
                if not expression:
                    print(f"⛔ Tabela '{nome_tabela_modelo_pbi}' não possui 'expression'.")
                    continue

                schema_db = banco = tabela_origem = conexao = ""

                for linha in expression:
                    if "PostgreSQL.Database" in linha:
                        conexao = "postgresql"
                        partes = linha.split("\"")
                        if len(partes) >= 3:
                            banco = partes[3]

                    if "Schema=" in linha and "Item=" in linha:
                        match_schema = re.search(r'Schema\s*=\s*"([^"]+)"', linha)
                        match_item = re.search(r'Item\s*=\s*"([^"]+)"', linha)
                        if match_schema:
                            schema_db = match_schema.group(1)
                        if match_item:
                            tabela_origem = match_item.group(1)

                if not all([schema_db, banco, tabela_origem, conexao]):
                    print(f"⚠️ Dados incompletos na tabela '{nome_tabela_modelo_pbi}', pulando.")
                    continue

                TabelaSemantica.objects.create(
                    nome_modelo_pbi=nome_modelo_pbi,
                    nome_tabela_modelo_pbi=nome_tabela_modelo_pbi,
                    nome_tabela_origem_db=tabela_origem,
                    schema=schema_db,
                    banco=banco,
                    conexao=conexao
                )
                registros_criados += 1

            return Response({"mensagem": f"{registros_criados} tabelas importadas com sucesso"}, status=200)

        except Exception as e:
            return Response({"erro": str(e)}, status=500)
