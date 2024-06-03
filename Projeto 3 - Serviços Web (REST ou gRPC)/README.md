1. Back-end: Python, PostgreSQL, SSE
2. Front-end: Flask

Dependências:
- Python3
- Flask
  - pip install flask
- Flask CORS
  - pip install flask_cors
- Psycopg2
  - pip install psycopg2
- dotenv
  - pip install python-dotenv
- PostgreSQL
  - sudo apt install postgresql postgresql-contrib
  - pip install https://ftp.postgresql.org/pub/pgadmin/pgadmin4/v8.7/pip/pgadmin4-8.7-py3-none-any.whl
- SQLite (?)
  - pip install sqlite3

Criando e ativando um ambiente virtual:

1. python3 -m venv venv
2. source venv/bin/activate

Para usar o PostgreSQL:
1. Instale o PostgreSQL (com apt install)
2. $ sudo -i -u postgres
3. $ psql
4. '#' \q

Glossário:
API REST (RESTful) - interface de programação de aplicações de transferência de estados representacional. Utiliza os princípios e operações CRUD (Create, Read, Update, Delete) e os métodos GET, POST, PUT, DELETE. 
Flask - é um pequeno framework (microframework) web escrito em Python que não requer ferramentas ou bibliotecas particulares
PostgreSQL - sistema gerenciador de banco de dados objeto relacional (SGBD)
SSE - conjunto de serviços de segurança em uma arquitetura SASE (independente da plataforma, permitindo a infraestrutura de segurança mais flexível possível).
