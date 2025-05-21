# Livraria Virtual - CRUD de Livros com Docker

## Visão Geral da Aplicação

Esta aplicação simula uma livraria virtual com funcionalidades de cadastro, edição, listagem e exclusão de livros. Foi desenvolvida com três componentes principais: frontend em Vue.js, backend em FastAPI, e banco de dados PostgreSQL. Todos os componentes são orquestrados com Docker Compose para facilitar a execução e integração.

## Contêineres e Tecnologias Utilizadas

* **frontend**: Vue 3 + Vite, servido por Nginx
* **backend**: FastAPI com SQLAlchemy e Uvicorn
* **db**: PostgreSQL 15

## Arquivos Obrigatórios

* `frontend/Dockerfile` - build e serviço do frontend
* `backend/Dockerfile` - API com FastAPI
* `docker-compose.yml` - composição dos três serviços
* `frontend/` - código-fonte do Vue
* `backend/` - código-fonte do FastAPI (com schemas, models, crud)
* `README.md` - instruções e documentação

## Manual de Instalação e Execução

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/livraria-docker.git
cd livraria-docker
```

2. Construa os contêineres:

```bash
docker compose build
```

3. Suba os serviços:

```bash
docker compose up -d
```

4. Acesse:

* Frontend: [http://localhost:8080](http://localhost:8080)
* Backend API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Estrutura do Projeto

```
livraria-docker/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── crud.py
│   │   ├── models.py
|   |   ├── seed.py
│   │   ├── schemas.py
│   │   └── database.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   └── components/ListaLivros.vue
│   ├── public/favicon.png
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
└── README.md
```

## Justificativa do Uso de 3 Contêineres

Atendendo aos requisitos da atividade, esta aplicação possui 3 contêineres:

1. **Frontend (Vue + Nginx)**
2. **Backend (FastAPI)**
3. **Banco de Dados (PostgreSQL)**

Cada contêiner comunica-se via nome de serviço definido no Docker Compose (ex: `db`, `backend`). Nenhuma comunicação usa localhost, conforme solicitado.

## Equipe

* Nome: Cleidson Almeida

## Licença

Este projeto é apenas para fins acadêmicos.

---

> Para mais detalhes, consulte os códigos nos diretórios `backend/` e `frontend/`.

