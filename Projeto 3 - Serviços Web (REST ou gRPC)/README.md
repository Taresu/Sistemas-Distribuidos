O Projeto 3 é uma aplicação web com métodos de inserção, consulta, atualização e exclusão de dados.

A aplicação provê a comunicação entre cliente e servidor, sendo definida da seguinte forma:

1. Back-end: Python, PostgreSQL (p/ o banco de dados), SSE (p/ envio de notificações)
2. Front-end: Flask e Express

Dependências do projeto:
- Python3
- Flask
  - pip install flask
- Flask CORS
  - pip install flask_cors
- Psycopg2
  - pip install psycopg2
- dotenv
  - pip install python-dotenv
- PostgreSQL & pgadmin4
  - sudo apt install postgresql postgresql-contrib
  - pip install https://ftp.postgresql.org/pub/pgadmin/pgadmin4/v8.7/pip/pgadmin4-8.7-py3-none-any.whl
- Redis
  - sudo service redis-server start
  - redis-cli
  - ping
  - curl http://localhost:5000/stream (novo terminal)
- Node-forge
  - npm install node-forge

Passos de execução da aplicação:
1. Iniciar o flask (dentro do ambiente virtual de 'API REST') - porta 5000
   - cd 'Projeto 3 - Serviços Web (REST ou gRPC)/API REST'
   - source venv/bin/activate
   - export FLASK_APP=routes.py
   - export FLASK_ENV=development
   - flask run
   - http://127.0.0.1/5000
2. Iniciar o pgadmin (dentro do ambiente virtual de 'API REST') - porta 5050
   - cd 'Projeto 3 - Serviços Web (REST ou gRPC)/API REST'
   - source venv/bin/activate
   - python3 venv/lib/python3.10/site-packages/pgadmin4/pgAdmin4.py
   - http://127.0.0.1/5050
3. Testar queries com Postman
4. Executar o cliente da aplicação e testar queries - porta 3000

Criando e ativando um ambiente virtual:

1. python3 -m venv venv
2. source venv/bin/activate

OBS: o ambiente virtual (venv) criado para o projeto está em 'API REST', então o comando 2 deve ser executado neste diretório, pois já possui a pasta 'venv', com toda a configuração necessária para a execução.

Para usar o PostgreSQL:
1. Instale o PostgreSQL (com apt install)
2. $ sudo -i -u postgres
3. $ psql
4. '#' \q
5. ALTER USER postgres WITH PASSWORD 'postgres';

OBS: é interessante utilizar o Postman para testar as querys. É preciso instalar o Postman Desktop para o reconhecimento do banco de dados local.

Glossário:
- API REST (RESTful) - interface de programação de aplicações de transferência de estados representacional. Utiliza os princípios e operações CRUD (Create, Read, Update, Delete) e os métodos GET, POST, PUT, DELETE.
- Flask - é um pequeno framework (microframework) web escrito em Python que não requer ferramentas ou bibliotecas particulares
- PostgreSQL - sistema gerenciador de banco de dados objeto relacional (SGBD)
- SSE - conjunto de serviços de segurança em uma arquitetura SASE (independente da plataforma, permitindo a infraestrutura de segurança mais flexível possível).
