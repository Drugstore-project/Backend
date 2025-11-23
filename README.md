# Drugstore Project - Backend API

## 📋 Sobre o Projeto
Este é o backend do sistema de gerenciamento de farmácia **PharmaCare**. Ele fornece uma API RESTful robusta construída com **FastAPI** para gerenciar todas as operações do sistema, incluindo controle de estoque, gestão de usuários, vendas, clientes e pedidos de reposição.

O projeto foi alinhado seguindo princípios de **Clean Architecture** e separação de responsabilidades, garantindo um código modular, testável e fácil de manter.

## 🚀 Tecnologias Utilizadas
- **Linguagem:** Python 3.10+
- **Framework:** FastAPI
- **Banco de Dados:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrações:** Alembic
- **Containerização:** Docker & Docker Compose
- **Testes:** Pytest

## 📂 Estrutura do Projeto
O projeto está organizado da seguinte forma:
- `app/api`: Endpoints da API (Routers).
- `app/crud`: Lógica de acesso ao banco de dados (Create, Read, Update, Delete).
- `app/models`: Modelos do SQLAlchemy (Tabelas do Banco).
- `app/schemas`: Schemas Pydantic para validação e serialização de dados.
- `app/core`: Configurações globais e segurança (Auth, JWT).
- `tests/`: Testes unitários e de integração.

## 🐳 Como Rodar com Docker (Recomendado)
O ambiente de desenvolvimento é totalmente dockerizado para facilitar a execução.

1. **Navegue até a pasta do backend:**
   ```bash
   cd Drugstore_Project/Backend/Backend
   ```

2. **Suba os containers (API + Banco de Dados + PgAdmin):**
   ```bash
   docker-compose up --build
   ```
   - A API estará disponível em: `http://localhost:8000`
   - A Documentação (Swagger) em: `http://localhost:8000/docs`
   - O PgAdmin (Gerenciador do Banco) em: `http://localhost:5050`

3. **Para parar os containers:**
   ```bash
   docker-compose down
   ```

## 🛠️ Como Rodar Localmente (Sem Docker)
Caso prefira rodar o Python localmente:

1. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   Certifique-se de ter um banco PostgreSQL rodando e configure o arquivo `.env` com a `DATABASE_URL`.

4. **Execute as migrações:**
   ```bash
   alembic upgrade head
   ```

5. **Inicie o servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🧪 Executando Testes
Para rodar a suíte de testes automatizados:

```bash
pytest
```
Ou via Docker:
```bash
docker-compose run tests
```