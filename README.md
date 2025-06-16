# BI Platform

Este projeto tem como objetivo criar uma plataforma de Business Intelligence onde os usuários podem importar modelos semânticos do Power BI (.pbit), extrair as tabelas com suas origens e armazenar as informações para análise e automação futura.

## 🛠 Tecnologias Utilizadas

- **Backend**: Django + Django REST Framework
- **Frontend**: Vue.js + Vite
- **Banco de Dados**: SQLite (em desenvolvimento)
- **Importação de Modelos**: Power BI `.pbit`

## 🚀 Funcionalidades

- Upload de arquivos `.pbit` do Power BI
- Extração do schema (`DataModelSchema`)
- Identificação de tabelas e suas respectivas origens (PostgreSQL, Google Sheets, BigQuery, etc.)
- Armazenamento dos metadados no banco de dados

## Como rodar localmente

```bash
# backend
cd bi_ai_platform
python manage.py runserver

# frontend
cd frontend
npm install
npm run dev
