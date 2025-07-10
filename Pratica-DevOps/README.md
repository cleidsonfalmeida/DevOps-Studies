# Livraria Virtual - CRUD de Livros com Docker

## Visão Geral da Aplicação

Esta aplicação simula uma livraria virtual com funcionalidades de cadastro, edição, listagem e exclusão de livros. Foi desenvolvida com três componentes principais: frontend em Vue.js, backend em FastAPI, e banco de dados PostgreSQL. Todos os componentes são orquestrados com Docker Compose para facilitar a execução e integração.

## Contêineres e Tecnologias Utilizadas

* **frontend**: Vue 3 + Vite, servido por Nginx
* **backend**: FastAPI com SQLAlchemy e Uvicorn
* **db**: PostgreSQL 15

### Dockerfile do Frontend (`frontend/Dockerfile`)

```Dockerfile
FROM node:18 AS build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

RUN rm -rf /usr/share/nginx/html/*

COPY --from=build /app/dist /usr/share/nginx/html

# Este arquivo foi necessário para fazer o proxy reverso
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Esse Dockerfile realiza uma build multiestágio. A primeira etapa usa Node.js para compilar os arquivos do Vue. A segunda etapa usa Nginx para servir os arquivos estáticos e também faz proxy para o backend.

---

### Dockerfile do Backend (`backend/Dockerfile`)

```Dockerfile
FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Esse Dockerfile prepara o ambiente com Python 3.10, instala as dependências da aplicação FastAPI e executa o servidor Uvicorn na porta 8000.

---

### docker-compose.yml

```yaml
version: "3.9"

services:

  db:
    image: postgres:15
    container_name: db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: livraria
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - livraria-net

  backend:
    build: ./backend
    container_name: backend
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://user:password@db:5432/livraria
    networks:
      - livraria-net

  frontend:
    build: ./frontend
    container_name: frontend
    depends_on:
      - backend
    ports:
      - "8080:80"
    networks:
      - livraria-net

volumes:
  postgres_data:

networks:
  livraria-net:
```

O arquivo `docker-compose.yml` orquestra os três serviços:

- `db`: container do PostgreSQL com persistência de dados usando volume.
- `backend`: container do FastAPI, que se comunica com o banco por nome (`db`).
- `nginx`: container que serve o frontend e redireciona chamadas `/api/` para o backend.

Todos os containers compartilham a mesma rede interna (`livraria-net`). Somente o Nginx expõe a porta 8080 para acesso externo.


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
git clone https://github.com/cleidsonfalmeida/DevOps-Studies.git

cd livraria-docker
```

2. Construa os contêineres e suba os serviços:

```bash
docker compose up --build
```

3. Acesse:

* Frontend: [http://localhost:8080](http://localhost:8080)

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

Este projeto possui licença GNU GENERAL PUBLIC LICENSE.

---

> Para mais detalhes, consulte os códigos nos diretórios `backend/` e `frontend/`.
